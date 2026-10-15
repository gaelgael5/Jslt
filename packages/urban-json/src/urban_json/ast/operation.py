"""Opérateurs du langage jslt.

Port de ``Bb.Jslt.Parser.OperationEnum`` (1:1).
"""

from __future__ import annotations

from enum import Enum, auto


class OperationEnum(Enum):
    """Opérateur binaire ou unaire (port de ``OperationEnum``)."""

    UNDEFINED = auto()

    GREATER_THAN = auto()  # >
    GREATER_THAN_OR_EQUAL = auto()  # >=
    EQUAL = auto()  # ==
    LESS_THAN_OR_EQUAL = auto()  # <=
    LESS_THAN = auto()  # <
    NOT_EQUAL = auto()  # !=

    ADD = auto()  # +
    SUBTRACT = auto()  # -
    DIVIDE = auto()  # /
    MODULO = auto()  # %
    MULTIPLY = auto()  # * (token WILDCARD_SUBSCRIPT)
    POWER = auto()  # ^ (XOR entier, cf. runtime .NET)

    CHAIN = auto()  # -> (injection d'argument de fonction, Phase 4)

    AND = auto()  # &  (ET bit-à-bit entier)
    AND_EXCLUSIVE = auto()  # && (ET booléen)
    OR = auto()  # |  (OU bit-à-bit entier)
    OR_EXCLUSIVE = auto()  # || (OU booléen)

    COALESCE = auto()  # ??

    NOT = auto()  # ! (unaire)
