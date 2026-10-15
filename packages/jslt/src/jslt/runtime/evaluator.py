"""Interpréteur d'AST jslt (tree-walking).

Analogue Python de l'étage d'exécution .NET (``OutputExpressionBuilder`` +
contexte d'exécution), mais sans génération de code : ce visiteur parcourt
l'AST et calcule directement la valeur résultante.

Il implémente l'interface :class:`jslt.ast.JsltJsonVisitor` ; chaque méthode
``visit_*`` renvoie la valeur JSON (structure Python) produite par le nœud.

Couverture actuelle : cas « défaut », JSONPath, variables, et boucles
(``$source`` / ``$where``). Opérateurs, casts et fonctions arrivent ensuite.
"""

from __future__ import annotations

from typing import Any

from jslt.ast import (
    JsltArray,
    JsltBase,
    JsltBinaryOperator,
    JsltConstant,
    JsltFunctionCall,
    JsltJsonVisitor,
    JsltObject,
    JsltOperator,
    JsltPath,
    JsltProperty,
    JsltSwitch,
    JsltSwitchCase,
    JsltVariable,
    OperationEnum,
)
from jslt.errors import JsltError

from .context import RuntimeContext
from .operators import apply_binary, apply_unary


class JsltEvaluationVisitor(JsltJsonVisitor):
    """Évalue un AST jslt contre un document source et renvoie le résultat."""

    def __init__(self, context: RuntimeContext) -> None:
        self.context = context

    def visit_object(self, node: JsltObject) -> dict[str, Any]:
        # Un objet porteur d'un $source construit un objet unique dont les chemins
        # internes se résolvent dans la projection de cette source.
        if node.source is not None:
            self.context.push_source(node.source.accept(self))
            try:
                return self._evaluate_object_body(node)
            finally:
                self.context.pop_source()
        return self._evaluate_object_body(node)

    def _evaluate_object_body(self, node: JsltObject) -> dict[str, Any]:
        """Construit l'objet (variables + propriétés) contre la source courante."""
        variables = list(node.variables)
        previous_scope = None
        if variables:
            # Les variables sont évaluées hâtivement, dans un scope propre à
            # l'objet (chaîné au scope parent), avant les propriétés — l'ordre
            # déclaration/usage dans l'objet est donc indifférent.
            previous_scope = self.context.push_scope()
            for variable in variables:
                value = variable.value.accept(self) if variable.value is not None else None
                self.context.variables.add(variable.name, value)

        try:
            result: dict[str, Any] = {}
            for prop in node.properties:
                result[prop.name] = prop.value.accept(self) if prop.value is not None else None
            return result
        finally:
            if previous_scope is not None:
                self.context.restore_scope(previous_scope)

    def visit_array(self, node: JsltArray) -> list[Any]:
        """Construit un tableau, en développant les items porteurs d'un $source.

        Un item (objet) avec ``$source`` est une boucle : on itère sur le tableau
        source et on produit une entrée par élément, l'élément devenant la source
        courante (``$where`` filtre). Un item sans ``$source`` est copié tel quel,
        éventuellement filtré par son ``$where``.
        """
        result: list[Any] = []
        for item in node.items:
            if item.source is not None:
                self._expand_loop(item, result)
            elif self._where_passes(item):
                result.append(item.accept(self))
        return result

    def _expand_loop(self, item: JsltBase, result: list[Any]) -> None:
        source_value = item.source.accept(self)
        if isinstance(source_value, list):
            elements = source_value
        elif source_value is None:
            elements = []
        else:
            # Lenient vs .NET (qui n'itère que les tableaux) : une source unique
            # produit une seule itération.
            elements = [source_value]

        for element in elements:
            self.context.push_source(element)
            try:
                if self._where_passes(item):
                    result.append(self._evaluate_loop_item(item))
            finally:
                self.context.pop_source()

    def _evaluate_loop_item(self, item: JsltBase) -> Any:
        # La source de l'item a déjà été consommée pour l'itération : on construit
        # son corps directement contre l'élément courant (sans la ré-appliquer).
        if isinstance(item, JsltObject):
            return self._evaluate_object_body(item)
        return item.accept(self)

    def _where_passes(self, item: JsltBase) -> bool:
        if item.where is None:
            return True
        return self._to_bool(item.where.accept(self))

    @staticmethod
    def _to_bool(value: Any) -> bool:
        """Conversion booléenne stricte, conforme à ``RuntimeContext.ConvertToBool``.

        Seul le booléen ``True`` est vrai ; toute autre valeur est fausse.
        """
        return value is True

    def visit_property(self, node: JsltProperty) -> Any:
        return node.value.accept(self) if node.value is not None else None

    def visit_constant(self, node: JsltConstant) -> Any:
        return node.value

    def visit_jpath(self, node: JsltPath) -> Any:
        """Applique le chemin JSONPath à sa racine.

        La racine est la valeur de la variable source (forme ``name:$.path``)
        lorsque ``node.variable`` est défini, sinon la source courante.

        Sémantique de ``RuntimeContext.GetContentByJPath`` (.NET) :
            * 0 correspondance -> ``None``
            * 1 correspondance -> la valeur
            * N correspondances -> la liste des valeurs
        """
        if node.variable is not None:
            _, root = self.context.variables.get(node.variable)
        else:
            root = self.context.current_source

        values = node.compiled.select_values(root)
        if not values:
            return None
        if len(values) == 1:
            return values[0]
        return values

    def visit_binary_operator(self, node: JsltBinaryOperator) -> Any:
        left = node.left.accept(self)

        # Coalesce : la gauche si elle n'est pas null, sinon la droite (la droite
        # n'est évaluée que si nécessaire — comme en .NET).
        if node.operator is OperationEnum.COALESCE:
            return left if left is not None else node.right.accept(self)

        if node.operator is OperationEnum.CHAIN:
            raise NotImplementedError("opérateur de chaînage '->' : Phase 4")

        right = node.right.accept(self)
        return apply_binary(left, node.operator, right)

    def visit_unary_operator(self, node: JsltOperator) -> Any:
        return apply_unary(node.operator, node.left.accept(self))

    def visit_function(self, node: JsltFunctionCall) -> Any:
        function = self.context.functions.get(node.name)
        if function is None:
            raise JsltError(f"fonction inconnue : {node.name}")
        path_args = self.context.functions.path_args_of(node.name)
        arguments = []
        for index, argument in enumerate(node.arguments):
            if index in path_args and isinstance(argument, JsltPath):
                # Argument « chemin » : passé compilé (non évalué), cf. distinct.
                arguments.append(argument.compiled)
            else:
                arguments.append(argument.accept(self))
        return function(self.context, *arguments)

    def visit_switch(self, node: JsltSwitch) -> Any:
        """Évalue un switch/when : premier cas dont la valeur égale l'expression,
        sinon ``default`` (sinon ``None``)."""
        left = node.expression.accept(self)
        for case in node.cases:
            right = case.right_expression.accept(self)
            if apply_binary(left, OperationEnum.EQUAL, right) is True:
                return case.accept(self)
        if node.default is not None:
            return node.default.accept(self)
        return None

    def visit_case(self, node: JsltSwitchCase) -> Any:
        return node.block.accept(self) if node.block is not None else None

    def visit_jvariable(self, node: JsltVariable) -> Any:
        """Résout une référence de variable depuis le scope courant.

        Conforme à ``RuntimeContext.GetVariable`` (.NET) : une variable inconnue
        résout à ``None`` (le moteur .NET émet en plus un avertissement non
        bloquant, à rebrancher quand le canal de diagnostic existera).
        """
        _, value = self.context.variables.get(node.name)
        return value
