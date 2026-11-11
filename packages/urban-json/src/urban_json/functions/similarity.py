"""Proximité de deux textes : ``levenshtein``, ``similarity``.

Sert à rapprocher deux écritures d'une même donnée (un nom saisi deux fois, un
libellé qui a changé de casse ou de ponctuation) — le cas que ni `==` ni
`foldtext` ne couvrent, parce qu'il reste une faute de frappe.

Aucune dépendance : l'algorithme tient en quinze lignes, et une dépendance de
plus dans le cœur se paierait à chaque installation.
"""

from __future__ import annotations

from typing import Any

from ._helpers import to_text
from .registry import jslt_function


def _distance(left: str, right: str) -> int:
    """Distance de Levenshtein, en mémoire O(min(n, m)).

    Deux lignes du tableau suffisent : on n'a jamais besoin de remonter le
    chemin d'édition, seulement de son coût. Sur des libellés de quelques
    dizaines de caractères, c'est instantané ; sur des textes très longs, cette
    fonction n'est pas l'outil (le coût reste en O(n·m) de temps).
    """
    if left == right:
        return 0
    if len(left) < len(right):
        left, right = right, left
    previous = list(range(len(right) + 1))
    for i, lchar in enumerate(left, start=1):
        current = [i]
        for j, rchar in enumerate(right, start=1):
            current.append(
                min(
                    previous[j] + 1,                               # suppression
                    current[j - 1] + 1,                            # insertion
                    previous[j - 1] + (lchar != rchar),            # substitution
                )
            )
        previous = current
    return previous[-1]


@jslt_function(
    "levenshtein",
    description="Nombre de caractères à insérer, supprimer ou remplacer pour passer d'un texte à l'autre",
    description_en="Number of characters to insert, delete or replace to go from one text to the other",
)
def execute_levenshtein(ctx: Any, left: Any = None, right: Any = None) -> Any:
    if left is None or right is None:
        return None
    return _distance(to_text(left), to_text(right))


@jslt_function(
    "similarity",
    description="Proximité de deux textes entre 0 (tout diffère) et 1 (identiques)",
    description_en="Closeness of two texts between 0 (all differs) and 1 (identical)",
)
def execute_similarity(ctx: Any, left: Any = None, right: Any = None) -> Any:
    """Distance ramenée à une proportion, plus facile à seuiller qu'un compte.

    Deux chaînes vides valent 1 : elles sont identiques. Rendre « indéfini »
    pour 0/0 obligerait chaque appelant à traiter ce cas, alors que la réponse
    est évidente.
    """
    if left is None or right is None:
        return None
    a, b = to_text(left), to_text(right)
    longest = max(len(a), len(b))
    if longest == 0:
        return 1.0
    return 1.0 - _distance(a, b) / longest
