"""Évaluation d'un argument paresseux contre un élément donné.

Partagé par toutes les fonctions qui calculent une expression **par élément**
(``sort``, ``distinctby``, ``partition``…). Un seul endroit, parce que deux
copies de cette poignée de lignes finiraient par traiter différemment le cas
« pas d'expression » ou l'empilement de la source — et le lecteur n'aurait aucun
moyen de savoir laquelle fait foi.
"""

from __future__ import annotations

from typing import Any


def evaluate_for(ctx: Any, item: Any, expression: Any) -> Any:
    """Évalue ``expression`` avec ``item`` pour source courante.

    Sans expression, l'élément lui-même fait office de valeur : ``sort($.l)``
    trie sur les éléments, ``distinctby($.l)`` dédupliquerait sur eux.
    """
    if expression is None:
        return item
    ctx.push_source(item)
    try:
        return expression()
    finally:
        ctx.pop_source()
