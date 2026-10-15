"""Segment d'un chemin JSONPath.

Port de ``Bb.JPaths.PathSegment`` : un segment regroupe des sélecteurs, peut
être récursif (``..``) et/ou en forme raccourcie (``.foo`` vs ``['foo']``).

La descente récursive (``is_recursive``) est en place structurellement mais sa
construction depuis la grammaire est réservée à la Phase 5.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .node import Node
from .selectors import ISelector


class PathSegment:
    """Segment de chemin (port de ``Bb.JPaths.PathSegment``)."""

    def __init__(
        self,
        selectors: Iterable[ISelector],
        *,
        is_recursive: bool = False,
        is_shorthand: bool = False,
    ) -> None:
        self.selectors: list[ISelector] = list(selectors)
        self.is_recursive = is_recursive
        self.is_shorthand = is_shorthand

    def evaluate(self, match: Node, root: Any) -> Iterable[Node]:
        if self.is_recursive:
            yield from self._recursively_evaluate(match, root)
        else:
            for selector in self.selectors:
                yield from selector.evaluate(match, root)

    def _recursively_evaluate(self, match: Node, root: Any) -> Iterable[Node]:
        for descendant in self._all_descendants(match):
            for selector in self.selectors:
                yield from selector.evaluate(descendant, root)

    @staticmethod
    def _all_descendants(match: Node) -> Iterable[Node]:
        yield match
        value = match.value
        if isinstance(value, dict):
            for key, member in value.items():
                child = match.child(member, key)
                yield from PathSegment._all_descendants(child)
        elif isinstance(value, list):
            for i, member in enumerate(value):
                child = match.child(member, i)
                yield from PathSegment._all_descendants(child)
