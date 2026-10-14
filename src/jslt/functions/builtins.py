"""Fonctions intégrées du cœur jslt.

Portage d'un sous-ensemble des ``CustomServices`` .NET. Chaque fonction reçoit le
contexte d'exécution en premier argument, puis les arguments JSON évalués.

Couverture actuelle : ``sum``, ``concat`` (4a) et ``convert`` (4b, support des
casts ``#type``). D'autres fonctions pures (distinct, count…) viendront ensuite ;
les fonctions d'E-S restent hors cœur.
"""

from __future__ import annotations

import json
from typing import Any

from jslt.errors import JsltError

from .registry import jslt_function


@jslt_function("sum")
def execute_sum(ctx: Any, token: Any = None) -> Any:
    """Somme des éléments numériques d'un tableau (port de ``ExecuteSum``).

    Un tableau vide ou ``None`` donne 0. La somme reste entière si tous les
    éléments sont entiers.
    """
    if token is None:
        return 0
    if isinstance(token, list):
        total: Any = 0
        for item in token:
            if isinstance(item, bool) or not isinstance(item, (int, float)):
                raise JsltError("sum attend des entiers ou des flottants")
            total += item
        return total
    if isinstance(token, (int, float)) and not isinstance(token, bool):
        return token
    raise JsltError("sum attend un tableau")


@jslt_function("concat")
def execute_concat(
    ctx: Any, token: Any = None, split_char: str | None = None, delimit_char: str | None = None
) -> str:
    """Concatène les éléments d'un tableau en chaîne (port de ``ExecuteConcat``).

    ``split_char`` et ``delimit_char`` composent le séparateur inséré entre les
    éléments (leur concaténation), vide par défaut.
    """
    separator = (split_char or "") + (delimit_char or "")
    if token is None:
        return ""
    if isinstance(token, list):
        return separator.join(_to_text(item) for item in token)
    return _to_text(token)


def _to_text(value: Any) -> str:
    if value is None:
        return ""
    if value is True:
        return "True"
    if value is False:
        return "False"
    return str(value)


# Valeurs par défaut par type cible (port de ``targetType.GetDefaultValue()``).
_DEFAULTS = {"integer": 0, "decimal": 0.0, "string": "", "boolean": False}


def _coerce_number(value: Any) -> float | int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return float(value)
    raise JsltError(f"conversion numérique impossible : {value!r}")


def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        low = value.strip().lower()
        if low in ("true", "false"):
            return low == "true"
    return bool(value)


@jslt_function("convert")
def execute_convert(ctx: Any, token: Any = None, target_type: str = "string") -> Any:
    """Convertit une valeur vers un type cible (port de ``ExecuteConvert``).

    ``target_type`` est le nom du type issu d'un cast ``#type`` (``integer``,
    ``decimal``, ``string``, ``boolean``, et de façon simplifiée ``uri`` /
    ``uuid`` / ``datetime`` / ``time`` rendus en chaîne).
    """
    if token is None:
        return _DEFAULTS.get(target_type)

    # Valeurs non scalaires : sérialisées en chaîne (comme le .NET).
    if isinstance(token, (dict, list)):
        return json.dumps(token, ensure_ascii=False, separators=(",", ":"))

    if target_type == "integer":
        return int(_coerce_number(token))
    if target_type == "decimal":
        return float(_coerce_number(token))
    if target_type == "boolean":
        return _coerce_bool(token)
    # string, et types temporels/identifiants rendus en texte (simplifié).
    return _to_text(token)
