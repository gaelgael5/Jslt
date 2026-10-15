"""Sélecteurs de segment JSONPath.

Port de ``Bb.JPaths`` (ISelector, NameSelector, IndexSelector).

Couverture : sélecteur de nom (``.name`` / ``['name']``), indice (``[0]``,
négatifs), wildcard (``*`` / ``[*]``) et slice (``[a:b]``). Le sélecteur de
filtre (``?(...)``) arrive en Phase 5b.
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


class PathFunctionSelector(ISelector):
    """Fonction de chemin appliquée au nœud courant (ex. ``@.tags.length()``).

    Port partiel des fonctions ``Bb.JPaths`` enregistrées : ``length`` (taille
    d'un objet/tableau, longueur d'une chaîne ; sinon rien) et ``value``
    (identité). ``count``/``match``/``search`` ne sont pas portées.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def evaluate(self, match: Node, root: Any) -> Iterable[Node]:
        if self.name == "length":
            value = match.value
            if isinstance(value, (dict, list, str)):
                yield match.child(len(value), "length()")
            # sinon : aucune valeur (null), comme LengthFunction
        elif self.name == "value":
            yield match  # valeur du nœud courant (identité)

    def build_string(self) -> str:
        return f"{self.name}()"

    def __repr__(self) -> str:
        return f"PathFunctionSelector({self.name!r})"


class WildcardSelector(ISelector):
    """Sélecteur wildcard ``*`` (port de ``Bb.JPaths.WildcardSelector``).

    Sélectionne toutes les valeurs d'un objet ou tous les éléments d'un tableau.
    """

    def evaluate(self, match: Node, root: Any) -> Iterable[Node]:
        node = match.value
        if isinstance(node, dict):
            for key, member in node.items():
                yield match.child(member, key)
        elif isinstance(node, list):
            for i, member in enumerate(node):
                yield match.child(member, i)

    def build_string(self) -> str:
        return "*"

    def __repr__(self) -> str:
        return "WildcardSelector()"


class SliceSelector(ISelector):
    """Sélecteur de tranche ``[start:end:step]`` (port de ``Bb.JPaths.SliceSelector``).

    Implémente l'algorithme de bornes du RFC 9535 (indices négatifs, pas négatif).
    """

    def __init__(self, start: int | None, end: int | None, step: int | None = None) -> None:
        self.start = start
        self.end = end
        self.step = step

    def evaluate(self, match: Node, root: Any) -> Iterable[Node]:
        node = match.value
        if not isinstance(node, list):
            return
        if self.step == 0:
            return

        count = len(node)
        step = self.step if self.step is not None else 1
        start = self.start if self.start is not None else (0 if step >= 0 else count)
        end = self.end if self.end is not None else (count if step >= 0 else -count - 1)
        lower, upper = self._bounds(start, end, step, count)

        if step > 0:
            i = lower
            while i < upper:
                yield match.child(node[i], i)
                i += step
        else:
            i = upper
            while lower < i:
                yield match.child(node[i], i)
                i += step

    @staticmethod
    def _normalize(index: int, length: int) -> int:
        return index if index >= 0 else length + index

    @classmethod
    def _bounds(cls, start: int, end: int, step: int, length: int) -> tuple[int, int]:
        start = cls._normalize(start, length)
        end = cls._normalize(end, length)
        if step >= 0:
            lower = min(max(start, 0), length)
            upper = min(max(end, 0), length)
        else:
            upper = min(max(start, -1), length - 1)
            lower = min(max(end, -1), length - 1)
        return lower, upper

    def build_string(self) -> str:
        base = f"{self.start if self.start is not None else ''}:{self.end if self.end is not None else ''}"
        return base if self.step is None else f"{base}:{self.step}"

    def __repr__(self) -> str:
        return f"SliceSelector({self.start}, {self.end}, {self.step})"
