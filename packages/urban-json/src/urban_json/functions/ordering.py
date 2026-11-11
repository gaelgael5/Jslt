"""Tri et ordre : ``sort``, ``reverse``, ``first``, ``last``.

Sans contrepartie .NET. La difficulté n'est pas le tri mais l'**ordre entre
types** : un tableau de données réelles mélange `null`, nombres et chaînes, et
un tri qui lève sur ``None < str`` serait inutilisable là où on en a le plus
besoin. On définit donc un ordre total, documenté, qui ne lève jamais.
"""

from __future__ import annotations

import json
from typing import Any

from urban_json.errors import JsltError

from ._helpers import is_number
from .registry import jslt_function

# Rangs de l'ordre total : null < booléens < nombres < chaînes < tableaux < objets.
_NULL, _BOOL, _NUMBER, _STRING, _ARRAY, _OBJECT = range(6)


def order_key(value: Any) -> tuple[int, Any]:
    """Clef de tri d'une valeur JSON quelconque.

    Le rang vient d'abord, donc deux types différents ne sont jamais comparés
    entre eux (le tuple s'arrête au premier élément). Tableaux et objets sont
    comparés sur leur JSON compact — arbitraire mais **stable** et reproductible,
    ce qui vaut mieux que de lever ou de les laisser dans un ordre d'exécution.
    """
    if value is None:
        return (_NULL, 0)
    if isinstance(value, bool):
        return (_BOOL, int(value))
    if is_number(value):
        return (_NUMBER, value)
    if isinstance(value, str):
        return (_STRING, value)
    if isinstance(value, list):
        return (_ARRAY, json.dumps(value, ensure_ascii=False, sort_keys=True))
    return (_OBJECT, json.dumps(value, ensure_ascii=False, sort_keys=True))


def _key_of(ctx: Any, item: Any, key: Any) -> Any:
    """Clef d'un élément : l'élément lui-même, ou l'expression de clef évaluée.

    L'expression est **paresseuse** (``lazy_args``) et évaluée avec l'élément
    comme source courante : ``sort($.items, $.prix)`` lit le prix de chaque
    élément, et ``sort($.noms, foldtext($))`` trie sur une clef calculée. C'est
    une convention **différente** de celle de ``distinct``, dont le chemin
    s'applique au tableau entier (``$.*.prix``) — là, impossible d'apparier une
    clef manquante avec son élément.
    """
    if key is None:
        return item
    ctx.push_source(item)
    try:
        return key()
    finally:
        ctx.pop_source()


@jslt_function(
    "sort",
    lazy_args=(1,),
    description=(
        "Trie un tableau : sur les éléments, ou sur une clef calculée par élément, "
        "du plus petit au plus grand (descending à true pour l'inverse)"
    ),
)
def execute_sort(ctx: Any, source: Any = None, key: Any = None, descending: Any = None) -> Any:
    """Tri **stable** d'un tableau (null et non-tableau donnent ``null``)."""
    if not isinstance(source, list):
        return None
    if descending is not None and not isinstance(descending, bool):
        raise JsltError(f"descending attend un booléen, reçu : {descending!r}")
    pairs = [(order_key(_key_of(ctx, item, key)), item) for item in source]
    # `list.sort` est stable, y compris avec reverse : à clefs égales, l'ordre
    # d'origine est conservé dans les deux sens.
    pairs.sort(key=lambda pair: pair[0], reverse=bool(descending))
    return [item for _, item in pairs]


@jslt_function("reverse", description="Inverse l'ordre des éléments d'un tableau, sans modifier la source")
def execute_reverse(ctx: Any, source: Any = None) -> Any:
    if not isinstance(source, list):
        return None
    return list(reversed(source))  # copie : le .NET mutait sa source dans `join`


@jslt_function("first", description="Premier élément d'un tableau, ou null s'il est vide")
def execute_first(ctx: Any, source: Any = None) -> Any:
    if not isinstance(source, list) or not source:
        return None
    return source[0]


@jslt_function("last", description="Dernier élément d'un tableau, ou null s'il est vide")
def execute_last(ctx: Any, source: Any = None) -> Any:
    if not isinstance(source, list) or not source:
        return None
    return source[-1]
