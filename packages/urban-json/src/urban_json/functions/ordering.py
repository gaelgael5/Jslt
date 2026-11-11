"""Tri et ordre : ``sort``, ``reverse``, ``first``, ``last``.

Sans contrepartie .NET. La difficulté n'est pas le tri mais l'**ordre entre
types** : un tableau de données réelles mélange `null`, nombres et chaînes, et
un tri qui lève sur ``None < str`` serait inutilisable là où on en a le plus
besoin. On définit donc un ordre total, documenté, qui ne lève jamais.
"""

from __future__ import annotations

import unicodedata
from functools import cmp_to_key
from typing import Any

from urban_json.errors import JsltError

from ._helpers import is_number
from ._lazy import evaluate_for
from .registry import jslt_function

# Rangs de l'ordre total : null < booléens < nombres < chaînes < tableaux < objets.
_NULL, _BOOL, _NUMBER, _STRING, _ARRAY, _OBJECT = range(6)


def order_key(value: Any) -> tuple[int, Any]:
    """Clef de tri d'une valeur JSON quelconque.

    Le rang vient d'abord, donc deux types différents ne sont jamais comparés
    entre eux (le tuple s'arrête au premier élément). Tableaux et objets sont
    comparés **élément par élément**, récursivement : chaque composante est
    elle-même une clef d'ordre, donc des types mélangés ne lèvent pas davantage
    à l'intérieur d'un tableau qu'au premier niveau. Un préfixe passe devant la
    séquence qu'il préfixe (``[1]`` avant ``[1, 1]``).

    Les comparer par leur JSON compact — ce que faisait la première version —
    revenait à les comparer par points de code : ``"[10]"`` passait avant
    ``"[2]"``. C'était invisible tant qu'on triait des scalaires, et faux dès
    qu'on écrivait un tri **multi-clefs** (``sort($.l, [$.a, $.b])``), qui est
    l'usage naturel d'une clef pouvant rendre un tableau.
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
        return (_ARRAY, tuple(order_key(item) for item in value))
    # Objet : les clés d'abord (triées, pour que l'ordre d'écriture ne compte
    # pas), puis les valeurs à clés égales.
    return (_OBJECT, tuple((key, order_key(value[key])) for key in sorted(value)))


# La clef d'un élément est évaluée par `evaluate_for` (cf. `_lazy`) : l'expression
# est paresseuse et vue avec l'élément pour source courante, donc
# `sort($.items, $.prix)` lit le prix de chaque élément et `sort($.noms,
# foldtext($))` trie sur une clef calculée. C'est une convention **différente**
# de celle de `distinct`, dont le chemin s'applique au tableau entier
# (`$.*.prix`) : là, une clef manquante ne pourrait plus être appariée à son
# élément.


@jslt_function(
    "sort",
    lazy_args=(1,),
    description=(
        "Trie un tableau : sur les éléments, ou sur une clef calculée par élément, "
        "du plus petit au plus grand (descending à true, ou un sens par clef, pour l'inverse)"
    ),
    description_en="Sorts an array: on the elements, or on a key computed per element, smallest first (descending true, or one direction per key, for the reverse)",
)
def execute_sort(ctx: Any, source: Any = None, key: Any = None, descending: Any = None) -> Any:
    """Tri **stable** d'un tableau (null et non-tableau donnent ``null``)."""
    if not isinstance(source, list):
        return None
    if isinstance(descending, list):
        return _sort_by_directions(ctx, source, key, descending)
    if descending is not None and not isinstance(descending, bool):
        raise JsltError(f"descending attend un booléen, reçu : {descending!r}")
    pairs = [(order_key(evaluate_for(ctx, item, key)), item) for item in source]
    # `list.sort` est stable, y compris avec reverse : à clefs égales, l'ordre
    # d'origine est conservé dans les deux sens.
    pairs.sort(key=lambda pair: pair[0], reverse=bool(descending))
    return [item for _, item in pairs]


def _sort_by_directions(ctx: Any, source: list, key: Any, descending: list) -> list:
    """Tri multi-clefs avec **un sens par clef** (``sort($.l, [$.a, $.b], [true, false])``).

    Un unique ``reverse`` ne sait pas le faire : il inverse l'ordre complet, donc
    toutes les clefs à la fois. On compare donc composante par composante, ce qui
    coûte une comparaison Python par couple au lieu d'un tri sur clefs — c'est le
    prix du sens par clef, et seule cette forme le paie. ``list.sort`` reste
    stable, y compris via ``cmp_to_key``.
    """
    for flag in descending:
        if not isinstance(flag, bool):
            raise JsltError(f"sort attend des booléens comme sens de tri, reçu : {flag!r}")
    rows: list[tuple[list, Any]] = []
    for item in source:
        parts = evaluate_for(ctx, item, key)
        if not isinstance(parts, list):
            # Un sens par clef n'a de sens qu'avec plusieurs clefs : accepter un
            # scalaire ici laisserait croire que le sens s'applique, alors qu'il
            # n'y a aucune position à ordonner.
            raise JsltError(f"sort avec un sens par clef attend une clef en tableau, reçue : {parts!r}")
        if len(descending) > len(parts):
            # La faute d'écriture la plus probable (un sens de trop) : sans ce
            # refus elle serait silencieuse et le tri paraîtrait juste.
            raise JsltError(f"sort : {len(descending)} sens de tri pour {len(parts)} clef(s)")
        rows.append(([order_key(part) for part in parts], item))
    rows.sort(key=cmp_to_key(lambda left, right: _compare_parts(left[0], right[0], descending)))
    return [item for _, item in rows]


def _compare_parts(left: list, right: list, descending: list) -> int:
    """Compare deux clefs composées, chaque position selon son propre sens."""
    for index in range(min(len(left), len(right))):
        if left[index] == right[index]:
            continue
        smaller = -1 if left[index] < right[index] else 1
        return -smaller if _descends(descending, index) else smaller
    if len(left) == len(right):
        return 0
    # Préfixe commun : la clef la plus courte passe devant, comme dans l'ordre
    # total des tableaux (`[1]` avant `[1, 1]`), et le sens de la position
    # manquante s'y applique aussi.
    shorter_first = -1 if len(left) < len(right) else 1
    return -shorter_first if _descends(descending, min(len(left), len(right))) else shorter_first


def _descends(descending: list, index: int) -> bool:
    """Sens de la position donnée ; au-delà de la liste fournie, croissant.

    Repli volontaire, aligné sur la forme scalaire où omettre ``descending`` veut
    dire croissant : donner moins de sens que de clefs n'est donc pas une faute,
    contrairement à en donner plus.
    """
    return index < len(descending) and descending[index]


@jslt_function(
    "reverse",
    description="Inverse l'ordre d'un tableau ou d'un texte, sans modifier la source",
    description_en="Reverses the order of an array or of a text, without modifying the source",
)
def execute_reverse(ctx: Any, source: Any = None) -> Any:
    if isinstance(source, str):
        # Inversion par **graphème** et non par point de code : sur « ané »
        # écrit en forme décomposée (e + accent combinant), inverser les points
        # de code collerait l'accent sur la lettre voisine.
        return "".join(reversed(_graphemes(source)))
    if not isinstance(source, list):
        return None
    return list(reversed(source))  # copie : le .NET mutait sa source dans `join`


def _graphemes(value: str) -> list[str]:
    """Découpe en caractères perçus : une base plus ses marques combinantes."""
    clusters: list[str] = []
    for char in value:
        if clusters and unicodedata.combining(char):
            clusters[-1] += char
        else:
            clusters.append(char)
    return clusters


@jslt_function("first", description="Premier élément d'un tableau, ou null s'il est vide", description_en="First element of an array, or null when it is empty")
def execute_first(ctx: Any, source: Any = None) -> Any:
    if not isinstance(source, list) or not source:
        return None
    return source[0]


@jslt_function("last", description="Dernier élément d'un tableau, ou null s'il est vide", description_en="Last element of an array, or null when it is empty")
def execute_last(ctx: Any, source: Any = None) -> Any:
    if not isinstance(source, list) or not source:
        return None
    return source[-1]
