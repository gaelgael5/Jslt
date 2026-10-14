"""Interpréteur d'AST jslt (tree-walking).

Analogue Python de l'étage d'exécution .NET (``OutputExpressionBuilder`` +
contexte d'exécution), mais sans génération de code : ce visiteur parcourt
l'AST et calcule directement la valeur résultante.

Il implémente l'interface :class:`jslt.ast.JsltJsonVisitor` ; chaque méthode
``visit_*`` renvoie la valeur JSON (structure Python) produite par le nœud.

Couverture actuelle (Phase 1 — cas « défaut ») : objets, tableaux et constantes
sont matérialisés tels quels. L'exploitation du document source (JSONPath,
variables, boucles, fonctions) arrive dans les phases suivantes.
"""

from __future__ import annotations

from typing import Any

from jslt.ast import (
    JsltArray,
    JsltConstant,
    JsltJsonVisitor,
    JsltObject,
    JsltPath,
    JsltProperty,
    JsltVariable,
)

from .context import RuntimeContext


class JsltEvaluationVisitor(JsltJsonVisitor):
    """Évalue un AST jslt contre un document source et renvoie le résultat."""

    def __init__(self, context: RuntimeContext) -> None:
        self.context = context

    def visit_object(self, node: JsltObject) -> dict[str, Any]:
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
        return [item.accept(self) for item in node.items]

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

    def visit_jvariable(self, node: JsltVariable) -> Any:
        """Résout une référence de variable depuis le scope courant.

        Conforme à ``RuntimeContext.GetVariable`` (.NET) : une variable inconnue
        résout à ``None`` (le moteur .NET émet en plus un avertissement non
        bloquant, à rebrancher quand le canal de diagnostic existera).
        """
        _, value = self.context.variables.get(node.name)
        return value
