"""Construire et retoucher un tableau : ``range``, ``slice``, ``append``,
``insert``, ``removeat``.

Sans contrepartie .NET. ``range`` est la seule fonction du moteur qui **crée**
une série : tout le reste transforme ce qui entre, et « les douze mois » ou
« 1 à N » étaient donc inexprimables si la donnée ne les portait pas.

Les retouches rendent toutes une **copie** : une fonction qui modifierait son
tableau d'entrée casserait les autres lectures du même document.
"""

from __future__ import annotations

from typing import Any

from urban_json.errors import JsltError

from ._helpers import coerce_number
from .registry import jslt_function

#: Au-delà, `range` refuse. Un template tourne sur une entrée qu'on ne choisit
#: pas (le playground l'exécute en bac à sable) et c'est le seul endroit où elle
#: peut demander un tableau d'un milliard d'éléments.
_MAX_RANGE = 1_000_000


@jslt_function(
    "range",
    description=(
        "Série d'entiers : range(fin), range(début, fin) ou range(début, fin, pas) ; "
        "la fin est exclue"
    ),
    description_en=(
        "A series of integers: range(end), range(start, end) or range(start, end, step); "
        "the end is excluded"
    ),
)
def execute_range(ctx: Any, start: Any = None, end: Any = None, step: Any = None) -> Any:
    """Convention de tous les langages : **fin exclue**, et un seul argument
    compte depuis zéro. ``range(3)`` rend ``[0, 1, 2]``, de sorte que la série
    s'aligne avec les indices de ``skip`` et de ``slice``."""
    first = 0 if end is None else int(coerce_number(start))
    last = int(coerce_number(start if end is None else end))
    increment = 1 if step is None else int(coerce_number(step))
    if increment == 0:
        raise JsltError("range : le pas ne peut pas être nul")
    length = max(0, -(-(last - first) // increment))
    if length > _MAX_RANGE:
        raise JsltError(f"range : série trop grande ({length} éléments, maximum {_MAX_RANGE})")
    return list(range(first, last, increment))


@jslt_function(
    "slice",
    description="Tranche d'un tableau de start à end exclu (indices négatifs depuis la fin)",
    description_en="Slice of an array from start to end excluded (negative indices from the end)",
)
def execute_slice(ctx: Any, source: Any = None, start: Any = 0, end: Any = None) -> Any:
    """Bornes **tolérantes**, comme ``substring`` : un template transforme des
    données qu'il ne choisit pas, et un tableau plus court que prévu ne doit pas
    faire échouer toute la transformation."""
    if not isinstance(source, list):
        return None
    first = int(coerce_number(start))
    if end is None:
        return source[first:]
    return source[first : int(coerce_number(end))]


@jslt_function(
    "append",
    description="Copie du tableau avec une valeur ajoutée à la fin",
    description_en="Copy of the array with a value added at the end",
)
def execute_append(ctx: Any, source: Any = None, value: Any = None) -> Any:
    """Ajoute **une** valeur : un tableau passé en second argument devient un
    élément imbriqué. Pour concaténer, c'est ``+`` ou ``union``."""
    if not isinstance(source, list):
        return None
    return [*source, value]


@jslt_function(
    "insert",
    description="Copie du tableau avec une valeur insérée à l'indice donné (négatif depuis la fin)",
    description_en="Copy of the array with a value inserted at the given index (negative from the end)",
)
def execute_insert(ctx: Any, source: Any = None, index: Any = 0, value: Any = None) -> Any:
    if not isinstance(source, list):
        return None
    result = list(source)
    result.insert(int(coerce_number(index)), value)
    return result


@jslt_function(
    "removeat",
    description="Copie du tableau privée de l'élément à l'indice donné (négatif depuis la fin)",
    description_en="Copy of the array without the element at the given index (negative from the end)",
)
def execute_removeat(ctx: Any, source: Any = None, index: Any = 0) -> Any:
    """Un indice hors bornes rend la copie **inchangée** plutôt que de lever :
    retirer ce qui n'est pas là n'a rien d'une faute, et c'est la même tolérance
    que ``slice`` et ``substring``."""
    if not isinstance(source, list):
        return None
    position = int(coerce_number(index))
    if not -len(source) <= position < len(source):
        return list(source)
    result = list(source)
    del result[position]
    return result
