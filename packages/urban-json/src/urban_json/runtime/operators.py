"""Sémantique des opérateurs jslt (port de ``RuntimeContext.EvaluateBinaryOperator``).

Le **type de l'opérande gauche** pilote la coercion de l'opérande droit, comme en
.NET. Les valeurs sont des types Python natifs.

Opérateurs portés :
    * comparaison : == != < <= > >=
    * arithmétique : + - * / %
    * ``^`` : XOR entier (et non une puissance — fidèle au runtime .NET)
    * ``&`` / ``|`` : ET / OU bit-à-bit entier
    * ``&&`` / ``||`` : ET / OU booléen
    * ``??`` (coalesce) et ``->`` (chain) sont traités par l'évaluateur, pas ici.

Écarts volontaires documentés vs .NET :
    * ``||`` (OrExclusive) : le .NET contient un copier-coller fautif qui applique
      un ET ; on applique un OU correct.
    * les arrondis exotiques de ``Convert.ToInt64`` (coercion d'un flottant en
      entier) ne sont pas répliqués ; les cas usuels (int/int, décimaux) le sont.
"""

from __future__ import annotations

from typing import Any

from urban_json.ast import OperationEnum


def _to_str(value: Any) -> str:
    if value is None:
        return ""
    if value is True:
        return "True"
    if value is False:
        return "False"
    return str(value)


def _to_number(value: Any) -> Any:
    if value is None:
        return 0
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return float(value)
    raise TypeError(f"valeur non convertible en nombre : {value!r}")


def _to_bool(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        low = value.strip().lower()
        if low == "true":
            return True
        if low == "false":
            return False
        return bool(value)
    return bool(value)


def _is_number(value: Any) -> bool:
    # En JSON/jslt un booléen n'est pas un nombre pour l'arithmétique.
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _equal(left: Any, right: Any) -> bool:
    if left is None:
        return right is None
    if isinstance(left, bool):
        return left == _to_bool(right)
    if isinstance(left, str):
        return left == _to_str(right)
    if isinstance(left, (int, float)):
        return left == _to_number(right)
    return False


def _compare(left: Any, right: Any, op: OperationEnum) -> bool:
    if not _is_number(left):
        return False
    right_num = _to_number(right)
    if op is OperationEnum.GREATER_THAN:
        return left > right_num
    if op is OperationEnum.GREATER_THAN_OR_EQUAL:
        return left >= right_num
    if op is OperationEnum.LESS_THAN:
        return left < right_num
    if op is OperationEnum.LESS_THAN_OR_EQUAL:
        return left <= right_num
    return False


def apply_binary(left: Any, operator: OperationEnum, right: Any) -> Any:
    """Évalue ``left operator right`` selon la sémantique jslt.

    ``COALESCE`` et ``CHAIN`` ne passent pas par ici (gérés par l'évaluateur).
    """
    if operator is OperationEnum.EQUAL:
        return _equal(left, right)
    if operator is OperationEnum.NOT_EQUAL:
        return not _equal(left, right)
    if operator in (
        OperationEnum.GREATER_THAN,
        OperationEnum.GREATER_THAN_OR_EQUAL,
        OperationEnum.LESS_THAN,
        OperationEnum.LESS_THAN_OR_EQUAL,
    ):
        return _compare(left, right, operator)

    if operator is OperationEnum.ADD:
        if isinstance(left, str):
            return left + _to_str(right)
        if _is_number(left):
            return left + _to_number(right)
        return False
    if operator is OperationEnum.SUBTRACT:
        return left - _to_number(right) if _is_number(left) else False
    if operator is OperationEnum.MULTIPLY:
        return left * _to_number(right) if _is_number(left) else False
    if operator is OperationEnum.DIVIDE:
        if not _is_number(left):
            return False
        right_num = _to_number(right)
        if isinstance(left, int) and isinstance(right_num, int):
            # Division entière tronquée vers zéro (comportement C#).
            return int(left / right_num)
        return left / right_num
    if operator is OperationEnum.MODULO:
        return left % _to_number(right) if _is_number(left) else False

    if operator is OperationEnum.POWER:  # ^ = XOR entier (cf. .NET)
        if _is_number(left):
            return int(left) ^ int(_to_number(right))
        return False
    if operator is OperationEnum.AND:  # & = ET bit-à-bit
        if _is_number(left):
            return int(left) & int(_to_number(right))
        return False
    if operator is OperationEnum.OR:  # | = OU bit-à-bit
        if _is_number(left):
            return int(left) | int(_to_number(right))
        return False

    if operator is OperationEnum.AND_EXCLUSIVE:  # && = ET booléen
        return _to_bool(left) and _to_bool(right)
    if operator is OperationEnum.OR_EXCLUSIVE:  # || = OU booléen (bug .NET corrigé)
        return _to_bool(left) or _to_bool(right)

    return None


def apply_unary(operator: OperationEnum, value: Any) -> Any:
    """Évalue un opérateur unaire (seule la négation ``!`` est définie)."""
    if operator is OperationEnum.NOT:
        return not _to_bool(value)
    return None
