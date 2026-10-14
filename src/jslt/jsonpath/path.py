"""Chemin JSONPath compilé.

Port de ``Bb.JPaths.JsonPath`` : un scope (global ``$`` ou local ``@``) et une
suite de segments. L'évaluation applique les segments l'un après l'autre à
partir du nœud racine, exactement comme le moteur .NET.
"""

from __future__ import annotations

from enum import Enum, auto
from typing import Any

from .node import Node
from .segment import PathSegment
from .selectors import IndexSelector, NameSelector


class PathScope(Enum):
    """Portée d'un chemin (port de ``Bb.JPaths.PathScope``)."""

    GLOBAL = auto()  # $
    LOCAL = auto()  # @


class JsonPath:
    """Chemin JSONPath compilé (port de ``Bb.JPaths.JsonPath``)."""

    def __init__(self, scope: PathScope, segments: list[PathSegment]) -> None:
        self.scope = scope
        self.segments = list(segments)

    @property
    def is_singular(self) -> bool:
        """Vrai si le chemin renvoie au plus une valeur (port de ``IsSingular``)."""
        return all(
            not seg.is_recursive
            and len(seg.selectors) == 1
            and isinstance(seg.selectors[0], (IndexSelector, NameSelector))
            for seg in self.segments
        )

    def evaluate(self, root: Any) -> list[Node]:
        """Applique le chemin au document ``root`` et renvoie la liste des nœuds."""
        current = [Node(root, ())]
        for segment in self.segments:
            nxt: list[Node] = []
            for node in current:
                nxt.extend(segment.evaluate(node, root))
            current = nxt
        return current

    def select_values(self, root: Any) -> list[Any]:
        """Renvoie uniquement les valeurs sélectionnées (équivalent SelectTokens)."""
        return [node.value for node in self.evaluate(root)]
