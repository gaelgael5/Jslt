"""Moteur JSONPath du portage jslt.

Port de ``Bb.JPaths`` (JSONPath RFC 9535, implémentation maison du moteur .NET).
Construit de façon incrémentale : la Phase 2a couvre les sélecteurs de nom et
d'indice ; wildcard, slice, descente récursive et filtres viendront en Phase 5.
"""

from .filter import (
    FilterBinary,
    FilterLiteral,
    FilterPath,
    FilterSelector,
    FilterUnary,
)
from .node import Node
from .path import JsonPath, PathScope
from .segment import PathSegment
from .selectors import (
    IndexSelector,
    ISelector,
    NameSelector,
    SliceSelector,
    WildcardSelector,
)

__all__ = [
    "FilterBinary",
    "FilterLiteral",
    "FilterPath",
    "FilterSelector",
    "FilterUnary",
    "ISelector",
    "IndexSelector",
    "JsonPath",
    "NameSelector",
    "Node",
    "PathScope",
    "PathSegment",
    "SliceSelector",
    "WildcardSelector",
]
