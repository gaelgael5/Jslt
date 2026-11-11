"""Agrégats : ``count``, ``avg``, ``median``, ``product``.

Le .NET n'offrait que ``sum``. Ces fonctions suivent sa convention : un élément
non numérique **lève** au lieu d'être ignoré — un agrégat qui saute
silencieusement les intrus donne un résultat plausible et faux, et le défaut de
données se découvre très loin de sa cause.

``min`` / ``max`` restent dans :mod:`.maths` (ils gardent leur forme binaire
.NET en plus de l'agrégat).

``groupby`` / ``countby`` / ``sumby`` / ``avgby`` vivent dans :mod:`.bykey` :
elles partagent une clef calculée par élément, pas la convention des agrégats.

``mode`` fait exception à la règle du refus : la valeur la plus fréquente d'un
libellé a un sens, et c'est son usage principal.
"""

from __future__ import annotations

import math
from typing import Any

from urban_json.errors import JsltError

from ._helpers import coerce_bool, coerce_number, is_number
from .ordering import order_key
from .registry import jslt_function


def numbers_of(token: Any, name: str) -> list[int | float] | None:
    """Éléments numériques d'un tableau, ou ``None`` si ``token`` est ``null``."""
    if token is None:
        return None
    if not isinstance(token, list):
        raise JsltError(f"{name} attend un tableau, reçu : {token!r}")
    for item in token:
        if not is_number(item):
            raise JsltError(f"{name} attend des entiers ou des flottants, reçu : {item!r}")
    return list(token)


@jslt_function(
    "count",
    description=(
        "Nombre d'éléments : éléments d'un tableau, clés d'un objet, caractères "
        "d'un texte, 0 pour null"
    ),
    description_en="Number of items: elements of an array, keys of an object, characters of a text, 0 for null",
)
def execute_count(ctx: Any, token: Any = None) -> int:
    """Taille d'une valeur, quelle qu'elle soit.

    Un scalaire compte pour 1 : c'est « une valeur », et rendre 0 laisserait
    croire à une absence. ``null`` vaut 0, lui, parce que c'est bien une absence.
    """
    if token is None:
        return 0
    if isinstance(token, (list, dict, str)):
        return len(token)
    return 1


@jslt_function("avg", description="Moyenne des nombres d'un tableau (null pour un tableau vide)", description_en="Mean of the numbers in an array (null for an empty array)")
def execute_avg(ctx: Any, token: Any = None) -> Any:
    values = numbers_of(token, "avg")
    if not values:
        # La moyenne de rien n'est pas 0 : `null` dit « pas de réponse ».
        return None
    return sum(values) / len(values)


@jslt_function("median", description="Valeur médiane des nombres d'un tableau (null pour un tableau vide)", description_en="Median value of the numbers in an array (null for an empty array)")
def execute_median(ctx: Any, token: Any = None) -> Any:
    values = numbers_of(token, "median")
    if not values:
        return None
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[middle]
    # Nombre pair : moyenne des deux valeurs centrales.
    return (ordered[middle - 1] + ordered[middle]) / 2


@jslt_function("product", description="Produit des nombres d'un tableau (1 pour un tableau vide)", description_en="Product of the numbers in an array (1 for an empty array)")
def execute_product(ctx: Any, token: Any = None) -> Any:
    values = numbers_of(token, "product")
    if values is None:
        return None
    total: Any = 1  # élément neutre, comme sum([]) vaut 0
    for value in values:
        total *= value
    return total


# --- dispersion et quantiles --------------------------------------------------


@jslt_function(
    "variance",
    description=(
        "Variance des nombres d'un tableau : de population par défaut, "
        "d'échantillon si sample vaut true"
    ),
    description_en="Variance of the numbers in an array: of population by default, of sample when sample is true",
)
def execute_variance(ctx: Any, token: Any = None, sample: Any = None) -> Any:
    """Variance, population par défaut.

    La population est le défaut parce qu'un template transforme **les données
    qu'on lui donne** : elles sont l'ensemble, pas un tirage. Qui veut la
    correction de Bessel la demande.
    """
    return _variance(numbers_of(token, "variance"), coerce_bool(sample))


def _variance(values: list | None, sample: bool) -> Any:
    if not values:
        return None
    divisor = len(values) - 1 if sample else len(values)
    if divisor <= 0:
        # Variance d'échantillon d'une seule valeur : n-1 = 0, la question n'a
        # pas de réponse. `null` le dit ; 0 affirmerait une dispersion nulle.
        return None
    moyenne = sum(values) / len(values)
    return sum((value - moyenne) ** 2 for value in values) / divisor


@jslt_function(
    "stddev",
    description=(
        "Écart-type des nombres d'un tableau : de population par défaut, "
        "d'échantillon si sample vaut true"
    ),
    description_en="Standard deviation of the numbers in an array: of population by default, of sample when sample is true",
)
def execute_stddev(ctx: Any, token: Any = None, sample: Any = None) -> Any:
    variance = _variance(numbers_of(token, "stddev"), coerce_bool(sample))
    return None if variance is None else math.sqrt(variance)


@jslt_function(
    "percentile",
    description="Centile p (0 à 100) des nombres d'un tableau, par interpolation linéaire",
    description_en="Percentile p (0 to 100) of the numbers in an array, by linear interpolation",
)
def execute_percentile(ctx: Any, token: Any = None, p: Any = None) -> Any:
    """Centile par **interpolation linéaire** entre les deux rangs encadrants.

    La méthode est explicite parce qu'il en existe neuf : celle-ci est celle de
    NumPy par défaut, et `percentile(v, 50)` coïncide donc avec `median`.
    """
    position = coerce_number(p) if is_number(p) else None
    if position is None or not 0 <= position <= 100:
        raise JsltError(f"centile attendu entre 0 et 100, reçu : {p!r}")
    values = numbers_of(token, "percentile")
    if not values:
        return None
    ordered = sorted(values)
    rank = position / 100 * (len(ordered) - 1)
    low, high = math.floor(rank), math.ceil(rank)
    if low == high:
        return ordered[low]
    return ordered[low] + (ordered[high] - ordered[low]) * (rank - low)


@jslt_function(
    "mode",
    description="Valeur la plus fréquente d'un tableau (la première apparue en cas d'égalité)",
    description_en="Most frequent value of an array (the first one seen in case of a tie)",
)
def execute_mode(ctx: Any, token: Any = None) -> Any:
    """Valeur modale, sur **n'importe quelles** valeurs.

    Contrairement aux autres agrégats, pas de refus des non-nombres : la valeur
    la plus fréquente d'un libellé ou d'un code a un sens, et c'est même l'usage
    principal. L'égalité est structurelle (clef d'ordre), et le premier apparu
    gagne — un départage par valeur dépendrait du type et surprendrait.
    """
    if not isinstance(token, list) or not token:
        return None
    counts: dict[Any, int] = {}
    first: dict[Any, Any] = {}
    for item in token:
        marker = order_key(item)
        counts[marker] = counts.get(marker, 0) + 1
        first.setdefault(marker, item)
    best = max(counts, key=lambda marker: counts[marker])
    return first[best]
