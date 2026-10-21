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


# --- implémentations par opérateur (callables (left, right) -> valeur) -------
# La sémantique est inchangée ; on la factorise ici pour deux usages : le
# dispatch de ``apply_binary`` (interpréteur) et la *pré-résolution* par le
# compilateur (``binary_op`` renvoie directement la callable de l'opérateur).

def _add(left: Any, right: Any) -> Any:
    if isinstance(left, str):
        return left + _to_str(right)
    if _is_number(left):
        return left + _to_number(right)
    return False


def _subtract(left: Any, right: Any) -> Any:
    return left - _to_number(right) if _is_number(left) else False


def _multiply(left: Any, right: Any) -> Any:
    return left * _to_number(right) if _is_number(left) else False


def _divide(left: Any, right: Any) -> Any:
    if not _is_number(left):
        return False
    right_num = _to_number(right)
    if isinstance(left, int) and isinstance(right_num, int):
        # Division entière tronquée vers zéro (comportement C#).
        return int(left / right_num)
    return left / right_num


def _modulo(left: Any, right: Any) -> Any:
    return left % _to_number(right) if _is_number(left) else False


def _xor(left: Any, right: Any) -> Any:  # ^ = XOR entier (cf. .NET)
    return int(left) ^ int(_to_number(right)) if _is_number(left) else False


def _bitand(left: Any, right: Any) -> Any:  # & = ET bit-à-bit
    return int(left) & int(_to_number(right)) if _is_number(left) else False


def _bitor(left: Any, right: Any) -> Any:  # | = OU bit-à-bit
    return int(left) | int(_to_number(right)) if _is_number(left) else False


_BINARY_DISPATCH: dict[OperationEnum, Any] = {
    OperationEnum.EQUAL: _equal,
    OperationEnum.NOT_EQUAL: lambda left, right: not _equal(left, right),
    OperationEnum.GREATER_THAN: lambda left, right: _compare(
        left, right, OperationEnum.GREATER_THAN),
    OperationEnum.GREATER_THAN_OR_EQUAL: lambda left, right: _compare(
        left, right, OperationEnum.GREATER_THAN_OR_EQUAL),
    OperationEnum.LESS_THAN: lambda left, right: _compare(
        left, right, OperationEnum.LESS_THAN),
    OperationEnum.LESS_THAN_OR_EQUAL: lambda left, right: _compare(
        left, right, OperationEnum.LESS_THAN_OR_EQUAL),
    OperationEnum.ADD: _add,
    OperationEnum.SUBTRACT: _subtract,
    OperationEnum.MULTIPLY: _multiply,
    OperationEnum.DIVIDE: _divide,
    OperationEnum.MODULO: _modulo,
    OperationEnum.POWER: _xor,
    OperationEnum.AND: _bitand,
    OperationEnum.OR: _bitor,
    OperationEnum.AND_EXCLUSIVE: lambda left, right: _to_bool(left) and _to_bool(right),
    OperationEnum.OR_EXCLUSIVE: lambda left, right: _to_bool(left) or _to_bool(right),
}


def binary_op(operator: OperationEnum) -> Any:
    """Renvoie la callable ``(left, right) -> valeur`` d'un opérateur binaire.

    Permet au compilateur de **pré-résoudre** l'opérateur à la compilation plutôt
    que de ré-aiguiller à chaque évaluation. ``None`` pour ``COALESCE`` / ``CHAIN``
    (gérés par l'évaluateur/compilateur, pas ici).
    """
    return _BINARY_DISPATCH.get(operator)


def apply_binary(left: Any, operator: OperationEnum, right: Any) -> Any:
    """Évalue ``left operator right`` selon la sémantique jslt.

    ``COALESCE`` et ``CHAIN`` ne passent pas par ici (gérés par l'évaluateur).
    """
    operation = _BINARY_DISPATCH.get(operator)
    if operation is None:
        return None
    return operation(left, right)


def apply_unary(operator: OperationEnum, value: Any) -> Any:
    """Évalue un opérateur unaire (seule la négation ``!`` est définie)."""
    if operator is OperationEnum.NOT:
        return not _to_bool(value)
    return None
