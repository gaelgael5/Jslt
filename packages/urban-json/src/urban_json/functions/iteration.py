"""Parcours d'un tableau par **expression** : ``map``, ``filter``, ``find``,
``findindex``, ``every``, ``some``, ``reduce``, ``minby``, ``maxby``, ``cumsum``.

Sans contrepartie .NET. Le moteur savait trier, grouper et agréger, mais la
boucle ``{"$source": …}`` — qui fait l'office de ``map`` — n'existe qu'en
**position de valeur** : impossible de la passer en argument d'une fonction.
D'où cette famille, qui repose entièrement sur les arguments **paresseux** déjà
en place (cf. :mod:`._lazy`) : l'expression est reçue non évaluée et calculée
une fois par élément, l'élément étant la source courante.

Convention de la famille, celle de ``limit`` : une source qui n'est pas un
tableau rend ``null`` — rendre ``[]`` ferait passer une erreur de chemin pour une
collection vide.
"""

from __future__ import annotations

from typing import Any

from urban_json.errors import JsltError

from ._helpers import coerce_bool, is_number
from ._lazy import evaluate_for
from .ordering import order_key
from .registry import jslt_function


@jslt_function(
    "map",
    lazy_args=(1,),
    description="Applique une expression à chaque élément d'un tableau et rend les résultats",
    description_en="Applies an expression to each element of an array and returns the results",
)
def execute_map(ctx: Any, source: Any = None, expression: Any = None) -> Any:
    """Ce que la boucle fait déjà, mais **en argument** d'une fonction."""
    if not isinstance(source, list):
        return None
    return [evaluate_for(ctx, item, expression) for item in source]


@jslt_function(
    "filter",
    lazy_args=(1,),
    description="Garde les éléments d'un tableau pour lesquels le prédicat est vrai",
    description_en="Keeps the elements of an array for which the predicate is true",
)
def execute_filter(ctx: Any, source: Any = None, predicate: Any = None) -> Any:
    """Le filtre JSONPath (`$.l[?(…)]`) couvre déjà le cas courant ; celui-ci
    accepte **n'importe quelle** expression, y compris un appel de fonction."""
    if not isinstance(source, list):
        return None
    return [item for item in source if coerce_bool(evaluate_for(ctx, item, predicate))]


@jslt_function(
    "find",
    lazy_args=(1,),
    description="Premier élément d'un tableau pour lequel le prédicat est vrai, sinon null",
    description_en="First element of an array for which the predicate is true, otherwise null",
)
def execute_find(ctx: Any, source: Any = None, predicate: Any = None) -> Any:
    if not isinstance(source, list):
        return None
    for item in source:
        if coerce_bool(evaluate_for(ctx, item, predicate)):
            return item
    return None


@jslt_function(
    "findindex",
    lazy_args=(1,),
    description="Position du premier élément qui satisfait le prédicat, -1 si aucun",
    description_en="Position of the first element satisfying the predicate, -1 when there is none",
)
def execute_findindex(ctx: Any, source: Any = None, predicate: Any = None) -> Any:
    if not isinstance(source, list):
        return None
    for index, item in enumerate(source):
        if coerce_bool(evaluate_for(ctx, item, predicate)):
            return index
    return -1


@jslt_function(
    "every",
    lazy_args=(1,),
    description="Vrai si le prédicat est vrai pour tous les éléments (vrai pour un tableau vide)",
    description_en="True when the predicate holds for every element (true for an empty array)",
)
def execute_every(ctx: Any, source: Any = None, predicate: Any = None) -> Any:
    """Vrai sur un tableau vide : il n'y a aucun contre-exemple. C'est la
    convention universelle, et elle surprend une fois sur deux — d'où le test."""
    if not isinstance(source, list):
        return None
    return all(coerce_bool(evaluate_for(ctx, item, predicate)) for item in source)


@jslt_function(
    "some",
    lazy_args=(1,),
    description="Vrai si le prédicat est vrai pour au moins un élément (faux pour un tableau vide)",
    description_en="True when the predicate holds for at least one element (false for an empty array)",
)
def execute_some(ctx: Any, source: Any = None, predicate: Any = None) -> Any:
    """``any`` dit « tableau non vide » (fidélité .NET) : il ne pouvait pas
    recevoir ce sens-ci, d'où un second nom plutôt qu'une rupture."""
    if not isinstance(source, list):
        return None
    return any(coerce_bool(evaluate_for(ctx, item, predicate)) for item in source)


@jslt_function(
    "reduce",
    lazy_args=(1,),
    description=(
        "Replie un tableau en une seule valeur ; l'expression voit "
        "{ acc, value, index } et rend le nouvel accumulateur"
    ),
    description_en=(
        "Folds an array into a single value; the expression sees "
        "{ acc, value, index } and returns the new accumulator"
    ),
)
def execute_reduce(ctx: Any, source: Any = None, expression: Any = None, initial: Any = None) -> Any:
    """Le seul repli général du moteur (``sum``, ``product``, ``sumby`` n'en sont
    que des cas particuliers).

    L'accumulateur et l'élément sont présentés **ensemble** comme source
    courante, ``{acc, value, index}`` : le langage n'a pas de second paramètre
    pour une expression, et inventer une variable implicite (``$acc``) aurait
    demandé la grammaire — donc Java, absent du conteneur.
    """
    if not isinstance(source, list):
        return None
    items = iter(source)
    accumulator = initial
    if initial is None:
        # Pas de valeur initiale : on part du premier élément, comme `sum` part
        # de son premier terme. Tableau vide, alors : `null`, il n'y a rien.
        accumulator = next(items, None)
        if accumulator is None:
            return None
        start = 1
    else:
        start = 0
    for index, item in enumerate(items, start=start):
        accumulator = evaluate_for(
            ctx, {"acc": accumulator, "value": item, "index": index}, expression
        )
    return accumulator


@jslt_function(
    "minby",
    lazy_args=(1,),
    description="Élément d'un tableau dont la clef calculée est la plus petite (null si vide)",
    description_en="Element of an array whose computed key is the smallest (null when empty)",
)
def execute_minby(ctx: Any, source: Any = None, key: Any = None) -> Any:
    return _extremum(ctx, source, key, largest=False)


@jslt_function(
    "maxby",
    lazy_args=(1,),
    description="Élément d'un tableau dont la clef calculée est la plus grande (null si vide)",
    description_en="Element of an array whose computed key is the largest (null when empty)",
)
def execute_maxby(ctx: Any, source: Any = None, key: Any = None) -> Any:
    return _extremum(ctx, source, key, largest=True)


def _extremum(ctx: Any, source: Any, key: Any, largest: bool) -> Any:
    """Rend l'**élément**, pas la clef : `max` rendait déjà la valeur extrême,
    ce qui ne dit pas *qui* la porte. L'ordre est le total de `sort`, donc il ne
    lève jamais sur des données mélangées, et l'égalité garde le premier venu."""
    if not isinstance(source, list) or not source:
        return None
    best = None
    best_key = None
    for item in source:
        marker = order_key(evaluate_for(ctx, item, key))
        if best_key is None or (marker > best_key if largest else marker < best_key):
            best, best_key = item, marker
    return best


@jslt_function(
    "cumsum",
    description="Totaux courants d'un tableau de nombres ([1,2,3] -> [1,3,6])",
    description_en="Running totals of an array of numbers ([1,2,3] -> [1,3,6])",
)
def execute_cumsum(ctx: Any, source: Any = None) -> Any:
    if not isinstance(source, list):
        return None
    total: Any = 0
    running: list = []
    for item in source:
        if not is_number(item):
            # Même refus que `sum` : un cumul qui saute un intrus est plausible
            # et faux, et la faute se découvre très loin de sa cause.
            raise JsltError(f"cumsum attend des nombres, reçu : {item!r}")
        total += item
        running.append(total)
    return running
