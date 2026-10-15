"""Fonctions intégrées « cœur » : sum, concat, convert, distinct.

Les autres familles (maths, texte, collections, encodage, divers) sont dans des
modules dédiés du paquet. Chaque fonction reçoit le contexte d'exécution en
premier argument, puis les arguments JSON évalués (ou un chemin compilé pour les
positions marquées ``path_args``).
"""

from __future__ import annotations

import json
from typing import Any

from jslt.errors import JsltError

from ._helpers import coerce_bool, coerce_number, to_text
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
        return separator.join(to_text(item) for item in token)
    return to_text(token)


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


# Valeurs par défaut par type cible (port de ``targetType.GetDefaultValue()``).
_DEFAULTS = {"integer": 0, "decimal": 0.0, "string": "", "boolean": False}


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
        return int(coerce_number(token))
    if target_type == "decimal":
        return float(coerce_number(token))
    if target_type == "boolean":
        return coerce_bool(token)
    # string, et types temporels/identifiants rendus en texte (simplifié).
    return to_text(token)
