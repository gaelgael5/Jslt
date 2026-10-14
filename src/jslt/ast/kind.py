"""Nature d'un nœud AST jslt.

Port de ``Bb.Jslt.Asts.JsltKind`` (Jslt/Asts/JsltKind.cs).
"""

from __future__ import annotations

from enum import Enum, auto


class JsltKind(Enum):
    """Nature d'un nœud de l'arbre jslt (1:1 avec l'enum .NET JsltKind)."""

    OBJECT = auto()
    PROPERTY = auto()
    DIRECTIVES = auto()
    ARRAY = auto()
    TIMESPAN = auto()
    URI = auto()
    GUID = auto()
    BYTES = auto()
    DATE = auto()
    NULL = auto()
    BOOLEAN = auto()
    STRING = auto()
    FLOAT = auto()
    INTEGER = auto()
    PATH = auto()
    FUNCTION = auto()
    PATH_PARENT = auto()
    PATH_KEY = auto()
    PATH_COALESCE = auto()
    JPATH = auto()
    PATH_INDICE = auto()
    TYPE = auto()
    OPERATOR = auto()
    JVARIABLE = auto()
    JTRANSLATE_VARIABLE = auto()
