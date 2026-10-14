"""Fonctions intégrées du cœur jslt.

Portage d'un sous-ensemble des ``CustomServices`` .NET. Chaque fonction reçoit le
contexte d'exécution en premier argument, puis les arguments JSON évalués.

Couverture actuelle : ``sum``, ``concat`` (4a) et ``convert`` (4b, support des
casts ``#type``). D'autres fonctions pures (distinct, count…) viendront ensuite ;
les fonctions d'E-S restent hors cœur.
"""

from __future__ import annotations

import json
import math
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


# --------------------------------------------------------------------- chaînes
# Convention .NET pour ces fonctions : None -> None, chaîne -> résultat, sinon
# False (valeur non chaîne).


def _string_result(token: Any, fn):
    if token is None:
        return None
    if isinstance(token, str):
        return fn(token)
    return False


@jslt_function("upper")
def execute_upper(ctx: Any, token: Any = None) -> Any:
    return _string_result(token, str.upper)


@jslt_function("lower")
def execute_lower(ctx: Any, token: Any = None) -> Any:
    return _string_result(token, str.lower)


@jslt_function("trim")
def execute_trim(ctx: Any, token: Any = None, txt: str | None = None) -> Any:
    return _string_result(token, lambda s: s.strip(txt) if txt else s.strip())


@jslt_function("split")
def execute_split(ctx: Any, token: Any = None, charset: str = "") -> Any:
    if token is None:
        return None
    if isinstance(token, str):
        return token.split(charset[0]) if charset else [token]
    return []


@jslt_function("startswith")
def execute_startswith(ctx: Any, token: Any = None, txt: str = "") -> Any:
    return _string_result(token, lambda s: s.startswith(txt))


@jslt_function("endswith")
def execute_endswith(ctx: Any, token: Any = None, txt: str = "") -> Any:
    return _string_result(token, lambda s: s.endswith(txt))


@jslt_function("stringcontains")
def execute_stringcontains(ctx: Any, token: Any = None, contain_str: str = "") -> Any:
    return _string_result(token, lambda s: contain_str in s)


# ----------------------------------------------------------------------- maths
# Convention .NET : une valeur non numérique (ou None) donne None.


def _number_result(token: Any, fn):
    if isinstance(token, bool) or not isinstance(token, (int, float)):
        return None
    return fn(token)


@jslt_function("abs")
def execute_abs(ctx: Any, token: Any = None) -> Any:
    return _number_result(token, abs)  # conserve int/float comme en .NET


@jslt_function("floor")
def execute_floor(ctx: Any, token: Any = None) -> Any:
    return _number_result(token, lambda n: float(math.floor(n)))  # .NET Math.Floor -> double


@jslt_function("round")
def execute_round(ctx: Any, token: Any = None) -> Any:
    # .NET Math.Round : arrondi bancaire (demi vers pair), comme round() de Python.
    return _number_result(token, lambda n: float(round(n)))


@jslt_function("min")
def execute_min(ctx: Any, left: Any = None, right: Any = None) -> Any:
    if isinstance(left, bool) or not isinstance(left, (int, float)):
        return None
    return float(min(left, _coerce_number(right)))  # .NET renvoie un double


@jslt_function("max")
def execute_max(ctx: Any, left: Any = None, right: Any = None) -> Any:
    if isinstance(left, bool) or not isinstance(left, (int, float)):
        return None
    return float(max(left, _coerce_number(right)))  # .NET renvoie un double


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


@jslt_function("distinct", path_args=(1,))
def execute_distinct(ctx: Any, source: Any = None, path: Any = None) -> list:
    """Déduplique les valeurs d'un tableau sélectionnées par un chemin.

    Port de ``ExecuteDistinct`` : ``source`` est le tableau, ``path`` un JSONPath
    (argument compilé, non évalué) appliqué à ``source`` pour sélectionner les
    clés uniques. Les scalaires sont dédupliqués par valeur ; objets et ``null``
    sont ignorés. L'ordre d'apparition est conservé.
    """
    if source is None or path is None:
        return []
    if not isinstance(source, list):
        return []

    result: list = []
    seen: set = set()
    for token in path.select_values(source):
        if token is None or isinstance(token, dict):
            continue  # null et objets ignorés (comme en .NET)
        key = (type(token).__name__, token if isinstance(token, (str, int, float)) else repr(token))
        if key not in seen:
            seen.add(key)
            result.append(token)
    return result


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
