"""Agrégats : ``count``, ``avg``, ``median``, ``product``.

Le .NET n'offrait que ``sum``. Ces fonctions suivent sa convention : un élément
non numérique **lève** au lieu d'être ignoré — un agrégat qui saute
silencieusement les intrus donne un résultat plausible et faux, et le défaut de
données se découvre très loin de sa cause.

``min`` / ``max`` restent dans :mod:`.maths` (ils gardent leur forme binaire
.NET en plus de l'agrégat).
"""

from __future__ import annotations

from typing import Any

from urban_json.errors import JsltError

from ._helpers import is_number
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


@jslt_function("avg", description="Moyenne des nombres d'un tableau (null pour un tableau vide)")
def execute_avg(ctx: Any, token: Any = None) -> Any:
    values = numbers_of(token, "avg")
    if not values:
        # La moyenne de rien n'est pas 0 : `null` dit « pas de réponse ».
        return None
    return sum(values) / len(values)


@jslt_function("median", description="Valeur médiane des nombres d'un tableau (null pour un tableau vide)")
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


@jslt_function("product", description="Produit des nombres d'un tableau (1 pour un tableau vide)")
def execute_product(ctx: Any, token: Any = None) -> Any:
    values = numbers_of(token, "product")
    if values is None:
        return None
    total: Any = 1  # élément neutre, comme sum([]) vaut 0
    for value in values:
        total *= value
    return total
