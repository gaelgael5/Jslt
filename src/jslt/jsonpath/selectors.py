"""Sélecteurs de segment JSONPath.

Port de ``Bb.JPaths`` (ISelector, NameSelector, IndexSelector).

Couverture actuelle (Phase 2a) : sélecteur de nom (``.name`` / ``['name']``) et
sélecteur d'indice (``[0]``, indices négatifs gérés comme en .NET). Les
sélecteurs wildcard (``*``), slice (``a:b``) et filtre (``?(...)``) arriveront en
Phase 5.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any

from .node import Node


class ISelector(ABC):
    """Sélecteur d'un segment de chemin (port de ``Bb.JPaths.ISelector``)."""

    @abstractmethod
    def evaluate(self, match: Node, root: Any) -> Iterable[Node]:
        """Évalue le sélecteur sur un nœud et renvoie les nœuds sélectionnés."""

    @abstractmethod
    def build_string(self) -> str:
        """Représentation textuelle du sélecteur (pour sérialisation / debug)."""


class NameSelector(ISelector):
    """Sélecteur de nom de propriété (port de ``Bb.JPaths.NameSelector``)."""

    def __init__(self, name: str) -> None:
        self.name = name

    def evaluate(self, match: Node, root: Any) -> Iterable[Node]:
        node = match.value
        if isinstance(node, dict) and self.name in node:
            yield match.child(node[self.name], self.name)

    def build_string(self) -> str:
        return f"'{self.name}'"

    def __repr__(self) -> str:
        return f"NameSelector({self.name!r})"


class IndexSelector(ISelector):
    """Sélecteur d'indice de tableau (port de ``Bb.JPaths.IndexSelector``)."""

    def __init__(self, index: int) -> None:
        self.index = index

    def evaluate(self, match: Node, root: Any) -> Iterable[Node]:
        node = match.value
        # En JSON, un booléen n'est pas un tableau ; isinstance(bool) exclu de facto.
        if not isinstance(node, list):
            return
        count = len(node)
        if self.index >= count:
            return
        if self.index < 0:
            adjusted = count + self.index
            if adjusted < 0:
                return
            yield match.child(node[adjusted], adjusted)
        else:
            yield match.child(node[self.index], self.index)

    def build_string(self) -> str:
        return str(self.index)

    def __repr__(self) -> str:
        return f"IndexSelector({self.index})"
