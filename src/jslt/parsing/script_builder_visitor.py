"""Construction de l'AST jslt à partir de l'arbre d'analyse ANTLR.

Port de ``Bb.Jslt.Parser.ScriptBuilderVisitor`` : la classe hérite du visiteur
ANTLR généré (``JsltParserVisitor``) et produit un arbre de :class:`jslt.ast`.
C'est la première des deux couches de visiteurs de l'architecture .NET (la
seconde opère sur l'AST : évaluation, sérialisation…).

Couverture actuelle (Phase 1 — cas « défaut ») : objets, tableaux, propriétés,
constantes (string, nombre, entier, booléen, null). Les constructions avancées
(chemins JSONPath, variables, fonctions, opérateurs, switch, casts) lèvent
``NotImplementedError`` en attendant leurs phases respectives.
"""

from __future__ import annotations

from typing import Any

from jslt._antlr.JsltParser import JsltParser
from jslt._antlr.JsltParserVisitor import JsltParserVisitor
from jslt.ast import (
    JsltArray,
    JsltBinaryOperator,
    JsltConstant,
    JsltFunctionCall,
    JsltKind,
    JsltObject,
    JsltOperator,
    JsltPath,
    JsltProperty,
    JsltSwitch,
    JsltSwitchCase,
    JsltVariable,
    OperationEnum,
)
from jslt.ast.location import TextLocation
from jslt.errors import JsltSemanticError
from jslt.jsonpath import (
    FilterBinary,
    FilterLiteral,
    FilterPath,
    FilterSelector,
    FilterUnary,
    IndexSelector,
    JsonPath,
    NameSelector,
    PathScope,
    PathSegment,
    SliceSelector,
    WildcardSelector,
)

# Clés spéciales reconnues dans un objet (port de la logique .NET VisitObj).
_SOURCE_NAMES = {"$", "$source"}
_WHERE_NAMES = {"?", "$where"}

# Texte d'opérateur -> OperationEnum (port de VisitOperation .NET).
_OPERATION_TOKENS = {
    "==": OperationEnum.EQUAL,
    ">=": OperationEnum.GREATER_THAN_OR_EQUAL,
    ">": OperationEnum.GREATER_THAN,
    "<=": OperationEnum.LESS_THAN_OR_EQUAL,
    "<": OperationEnum.LESS_THAN,
    "!=": OperationEnum.NOT_EQUAL,
    "+": OperationEnum.ADD,
    "-": OperationEnum.SUBTRACT,
    "/": OperationEnum.DIVIDE,
    "%": OperationEnum.MODULO,
    "*": OperationEnum.MULTIPLY,
    "^": OperationEnum.POWER,
    "&": OperationEnum.AND,
    "&&": OperationEnum.AND_EXCLUSIVE,
    "|": OperationEnum.OR,
    "||": OperationEnum.OR_EXCLUSIVE,
    "??": OperationEnum.COALESCE,
    "->": OperationEnum.CHAIN,
}

# Précédence standard (valeur haute = lie plus fort), associativité gauche.
# L'algorithme .NET regroupait par parité (non testé) ; on retient une
# précédence classique — choix propre documenté.
_PRECEDENCE = {
    OperationEnum.CHAIN: 8,
    OperationEnum.MULTIPLY: 7,
    OperationEnum.DIVIDE: 7,
    OperationEnum.MODULO: 7,
    OperationEnum.POWER: 7,
    OperationEnum.ADD: 6,
    OperationEnum.SUBTRACT: 6,
    OperationEnum.LESS_THAN: 5,
    OperationEnum.LESS_THAN_OR_EQUAL: 5,
    OperationEnum.GREATER_THAN: 5,
    OperationEnum.GREATER_THAN_OR_EQUAL: 5,
    OperationEnum.EQUAL: 4,
    OperationEnum.NOT_EQUAL: 4,
    OperationEnum.AND: 3,
    OperationEnum.OR: 3,
    OperationEnum.AND_EXCLUSIVE: 2,
    OperationEnum.OR_EXCLUSIVE: 1,
    OperationEnum.COALESCE: 0,
}

# Précédence des opérateurs dans un filtre JSONPath ?(...) : comparaison/in > & > |.
_FILTER_PRECEDENCE = {
    "==": 2, "!=": 2, "<": 2, "<=": 2, ">": 2, ">=": 2, "in": 2,
    "&": 1,
    "|": 0,
}


class ScriptBuilderVisitor(JsltParserVisitor):
    """Transforme l'arbre d'analyse ANTLR en AST jslt (:class:`jslt.ast.JsltBase`)."""

    # ------------------------------------------------------------------ script
    def visitScript(self, ctx: JsltParser.ScriptContext) -> Any:
        return self.visit(ctx.json())

    def visitJson(self, ctx: JsltParser.JsonContext) -> Any:
        return self.visit(ctx.jsonValue())

    def visitJsonValue(self, ctx: JsltParser.JsonValueContext) -> Any:
        if ctx.obj() is not None:
            return self.visit(ctx.obj())
        if ctx.array() is not None:
            return self.visit(ctx.array())
        return self.visit(ctx.jsonLtOperations())

    # -------------------------------------------------------------------- obj
    def visitObj(self, ctx: JsltParser.ObjContext) -> Any:
        result = JsltObject()
        result.location = TextLocation.from_ctx(ctx)

        for pair_ctx in ctx.pair():
            prop = self.visit(pair_ctx)
            if prop is None:
                continue

            name = prop.name
            if name.startswith("$") and name != "$directives":
                if name.startswith("$$"):
                    # Échappement : "$$x" devient la propriété littérale "$x".
                    prop.name = name[1:]
                    if result.has_property(prop.name):
                        raise JsltSemanticError(
                            f"la propriété '{prop.name}' existe déjà", location=prop.location
                        )
                    result.append(prop)
                elif name.lower() in _SOURCE_NAMES:
                    result.source = prop.value
                elif name.lower() in _WHERE_NAMES:
                    result.where = prop.value
                # autres clés $xxx : ignorées ici (directives : phases suivantes)
            else:
                if prop.kind == JsltKind.PROPERTY and result.has_property(name):
                    raise JsltSemanticError(
                        f"la propriété '{name}' existe déjà", location=prop.location
                    )
                result.append(prop)

        return result

    # ------------------------------------------------------------------ array
    def visitArray(self, ctx: JsltParser.ArrayContext) -> Any:
        items = ctx.jsonValue()
        result = JsltArray(len(items))
        result.location = TextLocation.from_ctx(ctx)

        for item_ctx in items:
            item = self.visit(item_ctx)
            if item is None:
                raise JsltSemanticError(
                    "valeur de tableau invalide", location=TextLocation.from_ctx(item_ctx)
                )
            result.items.append(item)

        return result

    # ------------------------------------------------------------------- pair
    def visitPair(self, ctx: JsltParser.PairContext) -> Any:
        name = self._string_text(ctx.string())

        value_ctx = ctx.jsonValue()
        if value_ctx is None:
            raise JsltSemanticError(
                f"valeur manquante pour la propriété {name}",
                location=TextLocation.from_ctx(ctx),
            )

        value = self.visit(value_ctx)
        if value is None:
            raise JsltSemanticError(
                f"valeur invalide pour la propriété {name}",
                location=TextLocation.from_ctx(ctx),
            )

        # Une clé finissant par ':' déclare une variable (port de VisitPair .NET).
        if name.endswith(":"):
            variable = JsltVariable(name=name[:-1], value=value)
            variable.location = TextLocation.from_ctx(ctx)
            return variable

        prop = JsltProperty(name=name, value=value)
        prop.location = TextLocation.from_ctx(ctx)
        return prop

    # ---------------------------------------------------------------- scalars
    def visitJsonValueString(self, ctx: JsltParser.JsonValueStringContext) -> Any:
        text = self._unescape(self._string_text(ctx.string()))
        node = JsltConstant(text, JsltKind.STRING)
        node.location = TextLocation.from_ctx(ctx)
        return self._with_optional_cast(node, ctx.jsonType())

    def visitJsonValueInteger(self, ctx: JsltParser.JsonValueIntegerContext) -> Any:
        # Ne lire que le token INT : ctx.getText() inclurait un éventuel #type.
        node = JsltConstant(int(ctx.INT().getText()), JsltKind.INTEGER)
        node.location = TextLocation.from_ctx(ctx)
        return self._with_optional_cast(node, ctx.jsonType())

    def visitJsonValueNumber(self, ctx: JsltParser.JsonValueNumberContext) -> Any:
        number = ctx.signedNumber() if ctx.signedNumber() is not None else ctx.signedInt()
        text = number.getText()
        if "." in text or "e" in text or "E" in text:
            node = JsltConstant(float(text), JsltKind.FLOAT)
        else:
            node = JsltConstant(int(text), JsltKind.INTEGER)
        node.location = TextLocation.from_ctx(ctx)
        return self._with_optional_cast(node, ctx.jsonType())

    def visitJsonValueBoolean(self, ctx: JsltParser.JsonValueBooleanContext) -> Any:
        node = JsltConstant(ctx.TRUE() is not None, JsltKind.BOOLEAN)
        node.location = TextLocation.from_ctx(ctx)
        return self._with_optional_cast(node, ctx.jsonType())

    def visitJsonValueNull(self, ctx: JsltParser.JsonValueNullContext) -> Any:
        node = JsltConstant(None, JsltKind.NULL)
        node.location = TextLocation.from_ctx(ctx)
        return node

    # ------------------------------------------------------- jsonLt (chaînage)
    def visitJsonLtOperations(self, ctx: JsltParser.JsonLtOperationsContext) -> Any:
        operands = [self.visit(sub) for sub in ctx.jsonLtOperation()]
        operators = [self.visit(op) for op in ctx.operation()]

        node = operands[0] if len(operands) == 1 else self._fold_operators(operands, operators, ctx)

        # Négation éventuelle portant sur toute l'expression (NT en tête).
        if ctx.NT() is not None:
            node = self._negate(node, ctx)
        return self._with_optional_cast(node, ctx.jsonType())

    def visitJsonLtOperation(self, ctx: JsltParser.JsonLtOperationContext) -> Any:
        item = ctx.jsonLtItem()
        node = self.visit(item) if item is not None else self.visit(ctx.jsonLtOperation())

        if ctx.NT() is not None:
            node = self._negate(node, ctx)
        return self._with_optional_cast(node, ctx.jsonType())

    def _negate(self, node, ctx) -> JsltOperator:
        operator = JsltOperator(node, OperationEnum.NOT)
        operator.location = TextLocation.from_ctx(ctx)
        return operator

    def _with_optional_cast(self, node, json_type_ctx):
        """Enveloppe ``node`` dans un appel ``convert`` si un cast ``#type`` suit.

        Port de ``GetConverter`` .NET : un cast devient ``convert(node, type)``.
        Le type est porté par une constante (nom du type, ex. ``integer``).
        """
        if json_type_ctx is None:
            return node
        type_name = json_type_ctx.getText().lstrip("#")
        type_const = JsltConstant(type_name, JsltKind.TYPE)
        type_const.location = TextLocation.from_ctx(json_type_ctx)
        call = JsltFunctionCall("convert", [node, type_const])
        call.location = TextLocation.from_ctx(json_type_ctx)
        return call

    def _fold_operators(self, operands, operators, ctx):
        """Construit l'arbre d'opérateurs par précédence standard (associativité
        gauche). L'algorithme .NET regroupait par parité (non testé) ; on retient
        une précédence classique, correcte et lisible.
        """
        operands = list(operands)
        operators = list(operators)
        while operators:
            # Opérateur de plus forte précédence, le plus à gauche à égalité.
            best = max(range(len(operators)), key=lambda i: (_PRECEDENCE[operators[i]], -i))
            left, right = operands[best], operands[best + 1]
            if operators[best] is OperationEnum.CHAIN:
                combined = self._apply_chain(left, right, ctx)
            else:
                combined = JsltBinaryOperator(left, operators[best], right)
                combined.location = TextLocation.from_ctx(ctx)
            operands[best : best + 2] = [combined]
            del operators[best]
        return operands[0]

    @staticmethod
    def _apply_chain(left, right, ctx):
        """Chaînage ``left -> f(...)`` : injecte ``left`` en tête des arguments de f.

        Port de l'``Inject`` du .NET (VisitJsonLtOperations, cas Chain).
        """
        if not isinstance(right, JsltFunctionCall):
            raise JsltSemanticError(
                "l'opérande droit de '->' doit être un appel de fonction",
                location=TextLocation.from_ctx(ctx),
            )
        right.inject(left, 0)
        return right

    def visitOperation(self, ctx: JsltParser.OperationContext) -> Any:
        return _OPERATION_TOKENS[ctx.getText()]

    def visitJsonLtItem(self, ctx: JsltParser.JsonLtItemContext) -> Any:
        if ctx.jsonfunctionCall() is not None:
            return self.visit(ctx.jsonfunctionCall())
        if ctx.jsltJsonpath() is not None:
            return self.visit(ctx.jsltJsonpath())
        if ctx.variable() is not None:
            return self.visit(ctx.variable())

        if ctx.jsonValueBoolean() is not None:
            return self.visit(ctx.jsonValueBoolean())
        if ctx.jsonValueString() is not None:
            return self.visit(ctx.jsonValueString())
        if ctx.jsonValueInteger() is not None:
            return self.visit(ctx.jsonValueInteger())
        if ctx.jsonValueNumber() is not None:
            return self.visit(ctx.jsonValueNumber())
        if ctx.jsonValueNull() is not None:
            return self.visit(ctx.jsonValueNull())

        raise NotImplementedError("item jslt non pris en charge en Phase 1")

    # -------------------------------------------------------------- variables
    def visitVariable(self, ctx: JsltParser.VariableContext) -> Any:
        # variable : VARIABLE_NAME jsonType?  (référence ; le ':' final est inclus)
        name = ctx.VARIABLE_NAME().getText()
        variable = JsltVariable(name=name.removesuffix(":"))
        variable.location = TextLocation.from_ctx(ctx)
        return self._with_optional_cast(variable, ctx.jsonType())

    # -------------------------------------------------------------- fonctions
    def visitJsonfunctionCall(self, ctx: JsltParser.JsonfunctionCallContext) -> Any:
        # jsonfunctionCall : jsonfunctionName ( jsonValueList? ) jsonType? obj?
        name = ctx.jsonfunctionName().getText()

        arguments: list = []
        if ctx.jsonValueList() is not None:
            arguments = self.visit(ctx.jsonValueList())

        # when/switch s'écrivent when(expr){ cas } : un bloc objet suit l'appel.
        if ctx.obj() is not None:
            if name.lower() not in ("when", "switch"):
                raise JsltSemanticError(
                    f"argument objet invalide pour la fonction {name}",
                    location=TextLocation.from_ctx(ctx),
                )
            if len(arguments) != 1:
                raise JsltSemanticError(
                    "when / switch n'accepte qu'un seul argument",
                    location=TextLocation.from_ctx(ctx),
                )
            return self._build_when(arguments[0], self.visit(ctx.obj()), ctx)

        call = JsltFunctionCall(name, arguments)
        call.location = TextLocation.from_ctx(ctx)
        return self._with_optional_cast(call, ctx.jsonType())

    def _build_when(self, expression, block: JsltObject, ctx) -> JsltSwitch:
        """Construit un JsltSwitch depuis when(expr){ cas } (port de BuildWhen)."""
        switch = JsltSwitch(expression)
        switch.location = TextLocation.from_ctx(ctx)
        for case in block.properties:
            if case.name.lower() == "default":
                switch.default = case.value
            else:
                right = JsltConstant(case.name, JsltKind.STRING)
                right.location = case.location
                switch.cases.append(JsltSwitchCase(right_expression=right, block=case.value))
        return switch

    def visitJsonValueList(self, ctx: JsltParser.JsonValueListContext) -> Any:
        return [self.visit(value) for value in ctx.jsonValue()]

    # --------------------------------------------------------------- jsonpath
    def visitJsltJsonpath(self, ctx: JsltParser.JsltJsonpathContext) -> Any:
        # jsltJsonpath : VARIABLE_NAME? jsonpath jsonType?
        variable_name = None
        if ctx.VARIABLE_NAME() is not None:
            variable_text = ctx.VARIABLE_NAME().getText()
            variable_name = variable_text.removesuffix(":")

        compiled = self._build_json_path(ctx.jsonpath())
        node = JsltPath(
            value=ctx.jsonpath().getText(), compiled=compiled, variable=variable_name
        )
        node.location = TextLocation.from_ctx(ctx)
        return self._with_optional_cast(node, ctx.jsonType())

    def _build_json_path(self, ctx: JsltParser.JsonpathContext) -> JsonPath:
        # jsonpath : DOLLAR jsonpath_subscript?
        segments: list[PathSegment] = []
        subscript = ctx.jsonpath_subscript()
        while subscript is not None:
            segments.append(self._build_segment(subscript))
            subscript = subscript.jsonpath_subscript()
        return JsonPath(PathScope.GLOBAL, segments)

    def _build_segment(self, ctx: JsltParser.Jsonpath_subscriptContext) -> PathSegment:
        # jsonpath_subscript :
        #     RECURSIVE_DESCENT (subscriptableBareword | subscriptables) jsonpath_subscript?
        #   | SUBSCRIPT subscriptableBareword jsonpath_subscript?
        #   | subscriptables jsonpath_subscript?
        if ctx.RECURSIVE_DESCENT() is not None:
            if ctx.subscriptableBareword() is not None:
                selector = self._build_bareword_selector(ctx.subscriptableBareword())
            else:
                selector = self._build_subscript_selector(ctx.subscriptables())
            return PathSegment([selector], is_recursive=True)

        if ctx.SUBSCRIPT() is not None:
            selector = self._build_bareword_selector(ctx.subscriptableBareword())
            return PathSegment([selector], is_shorthand=True)

        return PathSegment([self._build_subscript_selector(ctx.subscriptables())])

    @staticmethod
    def _build_bareword_selector(ctx: JsltParser.SubscriptableBarewordContext):
        # subscriptableBareword : jsonPath_identifier subscriptableArguments? | WILDCARD_SUBSCRIPT
        if ctx.WILDCARD_SUBSCRIPT() is not None:
            return WildcardSelector()
        if ctx.subscriptableArguments() is not None:
            raise NotImplementedError("fonction de chemin (size, contains…) : étape ultérieure")
        return NameSelector(ctx.jsonPath_identifier().getText())

    def _build_subscript_selector(self, ctx: JsltParser.SubscriptablesContext):
        # subscriptables : BRACKET_LEFT subscriptable BRACKET_RIGHT
        st = ctx.subscriptable()

        if st.STRING() is not None:
            return NameSelector(self._unescape(self._strip_quotes(st.STRING().getText(), '"')))
        if st.IDQUOTED() is not None:
            return NameSelector(self._strip_quotes(st.IDQUOTED().getText(), "'"))
        if st.WILDCARD_SUBSCRIPT() is not None:
            return WildcardSelector()
        if st.sliceable() is not None:
            return self._build_slice_selector(st.sliceable())
        if st.QUESTION() is not None:
            return FilterSelector(self._build_filter(st.expressions()))

        raise NotImplementedError("sélecteur de chemin non pris en charge")

    # --------------------------------------------------------- filtres ?(...)
    def _build_filter(self, ctx: JsltParser.ExpressionsContext):
        # expressions : NT? expression (binaryOperator expression)+ | ( expression )
        operands = [self._build_filter_expression(e) for e in ctx.expression()]
        operators = [op.getText() for op in ctx.binaryOperator()]
        unsupported = [op for op in operators if op not in _FILTER_PRECEDENCE]
        if unsupported:
            raise NotImplementedError(
                f"opérateur(s) de filtre non pris en charge : {', '.join(unsupported)}"
            )
        node = operands[0] if len(operands) == 1 else self._fold_filter(operands, operators)
        if ctx.NT() is not None:
            node = FilterUnary(node)
        return node

    def _build_filter_expression(self, ctx: JsltParser.ExpressionContext):
        # expression : jsonpath__ | NT expression | ( expression )
        if ctx.NT() is not None:
            return FilterUnary(self._build_filter_expression(ctx.expression()))
        if ctx.jsonpath__() is not None:
            return self._build_filter_operand(ctx.jsonpath__())
        return self._build_filter_expression(ctx.expression())

    def _build_filter_operand(self, ctx: JsltParser.Jsonpath__Context):
        # jsonpath__ : jsonpath_ | value
        if ctx.jsonpath_() is not None:
            return self._build_filter_path(ctx.jsonpath_())
        return FilterLiteral(self._literal_value(ctx.value()))

    def _build_filter_path(self, ctx: JsltParser.Jsonpath_Context) -> FilterPath:
        # jsonpath_ : (DOLLAR | CURRENT_VALUE) jsonpath_subscript?
        is_current = ctx.CURRENT_VALUE() is not None
        segments: list[PathSegment] = []
        subscript = ctx.jsonpath_subscript()
        while subscript is not None:
            segments.append(self._build_segment(subscript))
            subscript = subscript.jsonpath_subscript()
        return FilterPath(JsonPath(PathScope.GLOBAL, segments), is_current=is_current)

    def _literal_value(self, ctx: JsltParser.ValueContext):
        # value : STRING | IDQUOTED | signedNumber | TRUE | FALSE | NULL | obj | array | variable
        if ctx.STRING() is not None:
            return self._unescape(self._strip_quotes(ctx.STRING().getText(), '"'))
        if ctx.IDQUOTED() is not None:
            return self._strip_quotes(ctx.IDQUOTED().getText(), "'")
        if ctx.TRUE() is not None:
            return True
        if ctx.FALSE() is not None:
            return False
        if ctx.NULL() is not None:
            return None
        if ctx.signedNumber() is not None:
            text = ctx.signedNumber().getText()
            return float(text) if ("." in text or "e" in text or "E" in text) else int(text)
        if ctx.array() is not None:
            return self._const_from_node(self.visit(ctx.array()))
        if ctx.obj() is not None:
            return self._const_from_node(self.visit(ctx.obj()))
        raise NotImplementedError("littéral de filtre non pris en charge (variable)")

    def _const_from_node(self, node):
        """Convertit un sous-arbre AST **constant** (tableau/objet/constante) en
        valeur Python, pour un littéral de filtre (ex. ``@.n in [1, 2, 3]``)."""
        if isinstance(node, JsltConstant):
            return node.value
        if isinstance(node, JsltArray):
            return [self._const_from_node(item) for item in node.items]
        if isinstance(node, JsltObject):
            return {prop.name: self._const_from_node(prop.value) for prop in node.properties}
        raise NotImplementedError("littéral de filtre non constant non pris en charge")

    @staticmethod
    def _fold_filter(operands, operators):
        operands = list(operands)
        operators = list(operators)
        while operators:
            best = max(range(len(operators)), key=lambda i: (_FILTER_PRECEDENCE[operators[i]], -i))
            combined = FilterBinary(operands[best], operators[best], operands[best + 1])
            operands[best : best + 2] = [combined]
            del operators[best]
        return operands[0]

    @staticmethod
    def _build_slice_selector(ctx: JsltParser.SliceableContext):
        # sliceable : signedNumber | sliceableLeft | sliceableRight | sliceableBinary
        if ctx.signedNumber() is not None:
            return IndexSelector(int(ctx.signedNumber().getText()))
        if ctx.sliceableLeft() is not None:  # 'start:'
            start = int(ctx.sliceableLeft().signedNumber().getText())
            return SliceSelector(start, None)
        if ctx.sliceableRight() is not None:  # ':end'
            end = int(ctx.sliceableRight().signedNumber().getText())
            return SliceSelector(None, end)
        # sliceableBinary : 'start:end'
        numbers = ctx.sliceableBinary().signedNumber()
        return SliceSelector(int(numbers[0].getText()), int(numbers[1].getText()))

    @staticmethod
    def _strip_quotes(text: str, quote: str) -> str:
        if len(text) >= 2 and text.startswith(quote) and text.endswith(quote):
            return text[1:-1]
        return text

    # ---------------------------------------------------------------- helpers
    @staticmethod
    def _string_text(string_ctx: JsltParser.StringContext | None) -> str:
        """Texte d'un nœud ``string`` sans les guillemets englobants.

        Port de ``VisitString`` suivi du retrait des guillemets réalisé par les
        appelants .NET (VisitPair / VisitJsonValueString).
        """
        if string_ctx is None:
            return ""
        raw = string_ctx.getText().strip()
        if len(raw) >= 2 and raw.startswith('"') and raw.endswith('"'):
            raw = raw[1:-1]
        return raw

    @staticmethod
    def _unescape(text: str) -> str:
        """Déséchappe les séquences gérées par le moteur .NET (``\\\\`` et ``\\"``)."""
        result: list[str] = []
        i = 0
        length = len(text)
        while i < length:
            c = text[i]
            if c == "\\" and i + 1 < length:
                nxt = text[i + 1]
                if nxt in ('\\', '"', "t", "n", "r"):
                    result.append(nxt)
                    i += 2
                    continue
            result.append(c)
            i += 1
        return "".join(result)
