"""Expressions de filtre JSONPath ``[?(...)]``.

Analogue autonome du sous-système ``Bb.JPaths.Expressions`` du .NET (qui possède
son propre arbre d'expressions). On construit ici, depuis l'arbre ANTLR, un petit
arbre d'expressions évalué pour chaque élément du nœud filtré :

    * opérandes : chemin ``@...`` (élément courant) / ``$...`` (racine) ou littéral ;
    * comparaisons : ``== != < <= > >=`` ;
    * logiques : ``&`` (et), ``|`` (ou), ``!`` (négation) ;
    * appartenance : ``in`` (port de ``InOperator``).

Les autres opérateurs ensemblistes de la grammaire (``nin``, ``subsetof``,
``contains``, ``size``, ``empty``) ne sont pas implémentés — ils ne le sont pas
non plus dans le moteur de filtre .NET.
"""

from __future__ import annotations

import operator
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any

from .node import Node
from .selectors import ISelector

_COMPARATORS = {
    "==": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
}


def _single(values: list[Any]) -> Any:
    """0 correspondance -> None, 1 -> la valeur, N -> la liste (cf. GetContentByJPath)."""
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    return values


def _truthy(value: Any) -> bool:
    if value is None or value is False:
        return False
    return value != []


class FilterExpression(ABC):
    """Nœud d'une expression de filtre."""

    @abstractmethod
    def evaluate(self, root: Any, current: Any) -> Any: ...


class FilterLiteral(FilterExpression):
    def __init__(self, value: Any) -> None:
        self.value = value

    def evaluate(self, root: Any, current: Any) -> Any:
        return self.value


class FilterPath(FilterExpression):
    """Chemin relatif (``@``, racine locale) ou absolu (``$``, racine du document)."""

    def __init__(self, path: Any, is_current: bool) -> None:
        self.path = path  # jslt.jsonpath.JsonPath
        self.is_current = is_current

    def evaluate(self, root: Any, current: Any) -> Any:
        base = current if self.is_current else root
        return _single(self.path.select_values(base))


class FilterUnary(FilterExpression):
    def __init__(self, operand: FilterExpression) -> None:
        self.operand = operand

    def evaluate(self, root: Any, current: Any) -> Any:
        return not _truthy(self.operand.evaluate(root, current))


class FilterBinary(FilterExpression):
    def __init__(self, left: FilterExpression, operator_text: str, right: FilterExpression) -> None:
        self.left = left
        self.operator = operator_text
        self.right = right

    def evaluate(self, root: Any, current: Any) -> Any:
        if self.operator == "&":
            return _truthy(self.left.evaluate(root, current)) and _truthy(
                self.right.evaluate(root, current)
            )
        if self.operator == "|":
            return _truthy(self.left.evaluate(root, current)) or _truthy(
                self.right.evaluate(root, current)
            )

        left = self.left.evaluate(root, current)
        right = self.right.evaluate(root, current)

        if self.operator == "in":
            # Appartenance : la droite est une collection (port de InOperator).
            if isinstance(right, dict):
                return left in right.values()
            if isinstance(right, list):
                return left in right
            return False
        comparator = _COMPARATORS[self.operator]
        try:
            return comparator(left, right)
        except TypeError:
            # Types non comparables : égalité stricte pour ==/!=, faux sinon.
            if self.operator == "==":
                return left == right
            if self.operator == "!=":
                return left != right
            return False


class FilterSelector(ISelector):
    """Sélecteur de filtre (port de ``Bb.JPaths.FilterSelector``).

    Conserve les membres (valeurs d'objet / éléments de tableau) pour lesquels
    l'expression de filtre est vraie.
    """

    def __init__(self, expression: FilterExpression) -> None:
        self.expression = expression

    def evaluate(self, match: Node, root: Any) -> Iterable[Node]:
        node = match.value
        if isinstance(node, dict):
            for key, member in node.items():
                if _truthy(self.expression.evaluate(root, member)):
                    yield match.child(member, key)
        elif isinstance(node, list):
            for i, member in enumerate(node):
                if _truthy(self.expression.evaluate(root, member)):
                    yield match.child(member, i)

    def build_string(self) -> str:
        return "?(...)"

    def __repr__(self) -> str:
        return "FilterSelector(...)"
