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

from urban_json._text import to_text as _to_str
from urban_json.ast import OperationEnum
from urban_json.errors import JsltError


def _kind(value: Any) -> str:
    return "tableau" if isinstance(value, list) else "objet"


def _refuse_container(symbol: str, left: Any, right: Any, hint: str = "") -> None:
    """Refuse un opérateur qui n'a pas de réponse juste sur un conteneur.

    Ces opérateurs rendaient ``false`` — une **réponse**, donc invisible, et
    contradictoire pour les comparaisons : ``a < b`` et ``a >= b`` ne peuvent pas
    être faux ensemble. Le refus porte sur les tableaux et les objets seulement :
    ``null`` garde son repli à ``false`` (fidélité .NET), sur lequel des
    templates s'appuient.
    """
    for value in (left, right):
        if isinstance(value, (list, dict)):
            message = f"opérateur {symbol} inapplicable à un {_kind(value)}"
            raise JsltError(f"{message} : {hint}" if hint else message)


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
            pass
        try:
            return float(value)
        except ValueError as exc:
            # Message en français comme le reste des erreurs utilisateur : sans
            # cela, « could not convert string to float » remonte tel quel dans
            # le message de l'opération.
            raise JsltError(f"conversion numérique impossible : {value!r}") from exc
    raise JsltError(f"valeur non convertible en nombre : {value!r}")


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
    if isinstance(left, list):
        # Égalité **structurelle** : deux tableaux identiques se disaient
        # différents, et rien ne le signalait. Élément par élément avec la même
        # règle qu'au premier niveau (`"2" == 2` reste vrai), pour ne pas
        # introduire une troisième notion d'égalité dans le langage.
        return (
            isinstance(right, list)
            and len(left) == len(right)
            and all(_equal(a, b) for a, b in zip(left, right))
        )
    if isinstance(left, dict):
        # Mêmes clés (l'ordre d'écriture ne compte pas) et mêmes valeurs.
        return (
            isinstance(right, dict)
            and left.keys() == right.keys()
            and all(_equal(value, right[key]) for key, value in left.items())
        )
    return False


_COMPARISON_SYMBOLS = {
    OperationEnum.GREATER_THAN: ">",
    OperationEnum.GREATER_THAN_OR_EQUAL: ">=",
    OperationEnum.LESS_THAN: "<",
    OperationEnum.LESS_THAN_OR_EQUAL: "<=",
}


def _compare(left: Any, right: Any, op: OperationEnum) -> bool:
    _refuse_container(
        _COMPARISON_SYMBOLS.get(op, "<"),
        left,
        right,
        "l'ordre entre conteneurs est celui de sort(), pas celui des opérateurs",
    )
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
    if isinstance(left, list):
        if isinstance(right, list):
            # Deux tableaux se concatènent, comme deux chaînes : c'est la seule
            # lecture possible, et elle rendait `false`.
            return [*left, *right]
        # Concaténer ou ajouter un élément ? Les deux se défendent, donc on
        # refuse plutôt que de choisir en silence.
        raise JsltError(
            "opérateur + entre un tableau et une valeur : pour ajouter un élément, "
            "union([tableau, [valeur]])"
        )
    if isinstance(left, dict):
        # Fusionner deux objets demande de décider du profond et des tableaux :
        # `merge` porte ces options, un `+` muet les cacherait.
        raise JsltError("opérateur + entre deux objets : utiliser merge(gauche, droite)")
    return False


def _subtract(left: Any, right: Any) -> Any:
    _refuse_container("-", left, right)
    return left - _to_number(right) if _is_number(left) else False


def _multiply(left: Any, right: Any) -> Any:
    _refuse_container("*", left, right)
    return left * _to_number(right) if _is_number(left) else False


def _divide(left: Any, right: Any) -> Any:
    _refuse_container("/", left, right)
    if not _is_number(left):
        return False
    right_num = _to_number(right)
    if isinstance(left, int) and isinstance(right_num, int):
        # Division entière tronquée vers zéro (comportement C#).
        return int(left / right_num)
    return left / right_num


def _modulo(left: Any, right: Any) -> Any:
    _refuse_container("%", left, right)
    return left % _to_number(right) if _is_number(left) else False


def _xor(left: Any, right: Any) -> Any:  # ^ = XOR entier (cf. .NET)
    _refuse_container("^", left, right)
    return int(left) ^ int(_to_number(right)) if _is_number(left) else False


def _bitand(left: Any, right: Any) -> Any:  # & = ET bit-à-bit
    _refuse_container("&", left, right)
    return int(left) & int(_to_number(right)) if _is_number(left) else False


def _bitor(left: Any, right: Any) -> Any:  # | = OU bit-à-bit
    _refuse_container("|", left, right)
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


def _reported(operator: OperationEnum, operation: Any) -> Any:
    """Enveloppe un opérateur pour qu'un échec sorte en ``JsltError``.

    L'enveloppe est posée **ici**, dans la table, et non dans ``apply_binary`` :
    le compilateur pré-résout l'opérateur via ``binary_op`` et appelle la
    callable directement, donc une enveloppe posée côté interpréteur seul ferait
    diverger les deux chemins — une division par zéro restait une
    ``ZeroDivisionError`` brute en compilé, incatchable par ``trydefault``.
    """

    def reported(left: Any, right: Any) -> Any:
        try:
            return operation(left, right)
        except JsltError:
            raise
        except ZeroDivisionError as exc:
            raise JsltError(f"division par zéro : {left!r} {operator.name} {right!r}") from exc
        except (TypeError, ValueError) as exc:
            # Une opération impossible remontait en exception Python brute : ni
            # lisible dans un message, ni rattrapable par `trydefault`.
            raise JsltError(
                f"opération impossible : {left!r} {operator.name} {right!r} ({exc})"
            ) from exc

    return reported


_BINARY_REPORTED = {
    operator: _reported(operator, operation) for operator, operation in _BINARY_DISPATCH.items()
}


def binary_op(operator: OperationEnum) -> Any:
    """Renvoie la callable ``(left, right) -> valeur`` d'un opérateur binaire.

    Permet au compilateur de **pré-résoudre** l'opérateur à la compilation plutôt
    que de ré-aiguiller à chaque évaluation. ``None`` pour ``COALESCE`` / ``CHAIN``
    (gérés par l'évaluateur/compilateur, pas ici).
    """
    return _BINARY_REPORTED.get(operator)


def apply_binary(left: Any, operator: OperationEnum, right: Any) -> Any:
    """Évalue ``left operator right`` selon la sémantique jslt.

    ``COALESCE`` et ``CHAIN`` ne passent pas par ici (gérés par l'évaluateur).
    """
    operation = _BINARY_REPORTED.get(operator)
    if operation is None:
        return None
    return operation(left, right)


def apply_unary(operator: OperationEnum, value: Any) -> Any:
    """Évalue un opérateur unaire (seule la négation ``!`` est définie)."""
    if operator is OperationEnum.NOT:
        return not _to_bool(value)
    return None
