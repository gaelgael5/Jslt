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
from jslt.ast import JsltArray, JsltConstant, JsltKind, JsltObject, JsltPath, JsltProperty
from jslt.ast.location import TextLocation
from jslt.errors import JsltSemanticError
from jslt.jsonpath import (
    IndexSelector,
    JsonPath,
    NameSelector,
    PathScope,
    PathSegment,
)

# Clés spéciales reconnues dans un objet (port de la logique .NET VisitObj).
_SOURCE_NAMES = {"$", "$source"}
_WHERE_NAMES = {"?", "$where"}


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

        prop = JsltProperty(name=name, value=value)
        prop.location = TextLocation.from_ctx(ctx)
        return prop

    # ---------------------------------------------------------------- scalars
    def visitJsonValueString(self, ctx: JsltParser.JsonValueStringContext) -> Any:
        if ctx.jsonType() is not None:
            raise NotImplementedError("cast de type sur une chaîne : Phase 3")
        text = self._unescape(self._string_text(ctx.string()))
        node = JsltConstant(text, JsltKind.STRING)
        node.location = TextLocation.from_ctx(ctx)
        return node

    def visitJsonValueInteger(self, ctx: JsltParser.JsonValueIntegerContext) -> Any:
        if ctx.jsonType() is not None:
            raise NotImplementedError("cast de type sur un entier : Phase 3")
        node = JsltConstant(int(ctx.getText()), JsltKind.INTEGER)
        node.location = TextLocation.from_ctx(ctx)
        return node

    def visitJsonValueNumber(self, ctx: JsltParser.JsonValueNumberContext) -> Any:
        if ctx.jsonType() is not None:
            raise NotImplementedError("cast de type sur un nombre : Phase 3")
        text = ctx.getText()
        if "." in text or "e" in text or "E" in text:
            node = JsltConstant(float(text), JsltKind.FLOAT)
        else:
            node = JsltConstant(int(text), JsltKind.INTEGER)
        node.location = TextLocation.from_ctx(ctx)
        return node

    def visitJsonValueBoolean(self, ctx: JsltParser.JsonValueBooleanContext) -> Any:
        if ctx.jsonType() is not None:
            raise NotImplementedError("cast de type sur un booléen : Phase 3")
        node = JsltConstant(ctx.getText().lower() == "true", JsltKind.BOOLEAN)
        node.location = TextLocation.from_ctx(ctx)
        return node

    def visitJsonValueNull(self, ctx: JsltParser.JsonValueNullContext) -> Any:
        node = JsltConstant(None, JsltKind.NULL)
        node.location = TextLocation.from_ctx(ctx)
        return node

    # ------------------------------------------------------- jsonLt (chaînage)
    def visitJsonLtOperations(self, ctx: JsltParser.JsonLtOperationsContext) -> Any:
        operations = ctx.operation()
        sub_operations = ctx.jsonLtOperation()

        if operations:
            raise NotImplementedError("opérateurs binaires : Phase 3")
        if ctx.NT() is not None:
            raise NotImplementedError("opérateur de négation : Phase 3")
        if len(sub_operations) != 1:
            raise NotImplementedError("expression entre parenthèses : Phase 3")

        return self.visit(sub_operations[0])

    def visitJsonLtOperation(self, ctx: JsltParser.JsonLtOperationContext) -> Any:
        if ctx.jsonType() is not None:
            raise NotImplementedError("cast de type : Phase 3")
        if ctx.NT() is not None:
            raise NotImplementedError("opérateur de négation : Phase 3")

        item = ctx.jsonLtItem()
        if item is not None:
            return self.visit(item)

        sub = ctx.jsonLtOperation()
        if sub is not None:
            return self.visit(sub)

        raise NotImplementedError("opération jslt non prise en charge en Phase 1")

    def visitJsonLtItem(self, ctx: JsltParser.JsonLtItemContext) -> Any:
        if ctx.jsonfunctionCall() is not None:
            raise NotImplementedError("appel de fonction : Phase 4")
        if ctx.jsltJsonpath() is not None:
            return self.visit(ctx.jsltJsonpath())
        if ctx.variable() is not None:
            raise NotImplementedError("variable : Phase 2")

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

    # --------------------------------------------------------------- jsonpath
    def visitJsltJsonpath(self, ctx: JsltParser.JsltJsonpathContext) -> Any:
        # jsltJsonpath : VARIABLE_NAME? jsonpath jsonType?
        if ctx.VARIABLE_NAME() is not None:
            raise NotImplementedError("projection d'un chemin sur une variable : Phase 2b")
        if ctx.jsonType() is not None:
            raise NotImplementedError("cast de type sur un chemin : Phase 3")

        compiled = self._build_json_path(ctx.jsonpath())
        node = JsltPath(value=ctx.jsonpath().getText(), compiled=compiled)
        node.location = TextLocation.from_ctx(ctx)
        return node

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
            raise NotImplementedError("descente récursive '..' : Phase 5")

        if ctx.SUBSCRIPT() is not None:
            selector = self._build_bareword_selector(ctx.subscriptableBareword())
            return PathSegment([selector], is_shorthand=True)

        return PathSegment([self._build_subscript_selector(ctx.subscriptables())])

    @staticmethod
    def _build_bareword_selector(ctx: JsltParser.SubscriptableBarewordContext):
        # subscriptableBareword : jsonPath_identifier subscriptableArguments? | WILDCARD_SUBSCRIPT
        if ctx.WILDCARD_SUBSCRIPT() is not None:
            raise NotImplementedError("wildcard '*' : Phase 5")
        if ctx.subscriptableArguments() is not None:
            raise NotImplementedError("fonction de chemin : Phase 5")
        return NameSelector(ctx.jsonPath_identifier().getText())

    def _build_subscript_selector(self, ctx: JsltParser.SubscriptablesContext):
        # subscriptables : BRACKET_LEFT subscriptable BRACKET_RIGHT
        st = ctx.subscriptable()

        if st.STRING() is not None:
            return NameSelector(self._unescape(self._strip_quotes(st.STRING().getText(), '"')))
        if st.IDQUOTED() is not None:
            return NameSelector(self._strip_quotes(st.IDQUOTED().getText(), "'"))
        if st.sliceable() is not None:
            sliceable = st.sliceable()
            if sliceable.signedNumber() is not None:
                return IndexSelector(int(sliceable.signedNumber().getText()))
            raise NotImplementedError("slice '[a:b]' : Phase 5")
        if st.WILDCARD_SUBSCRIPT() is not None:
            raise NotImplementedError("wildcard '[*]' : Phase 5")

        raise NotImplementedError("sélecteur de chemin non pris en charge en Phase 2a")

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
