"""Choisir une valeur selon une condition : ``ifelse``.

Sans contrepartie .NET. Le langage n'a **aucune** conditionnelle en position
d'expression : ``when`` est un aiguillage sur une **valeur** (il compare par
``==`` à chaque cas), donc une condition composée — ``$.n > 10 && $.actif`` —
devait d'abord être calculée, puis aiguillée sur son texte (``"true"`` /
``"false"``). C'était le manque le plus élémentaire du moteur, et le seul sans
contournement lisible.

Une vraie conditionnelle dans la grammaire (``if … else``) demanderait de
modifier la grammaire ANTLR, donc ``java``, absent du conteneur ; les arguments
**paresseux** (cf. :mod:`._lazy`) suffisent à obtenir la même sémantique sous
forme de fonction : seule la branche retenue est évaluée.
"""

from __future__ import annotations

from typing import Any

from ._helpers import coerce_bool
from .registry import jslt_function


@jslt_function(
    "ifelse",
    lazy_args=(1, 2),
    description="Valeur de la 2e expression si la condition est vraie, sinon celle de la 3e (seule la branche retenue est évaluée)",
    description_en="Value of the 2nd expression when the condition is true, otherwise that of the 3rd (only the chosen branch is evaluated)",
)
def execute_ifelse(
    ctx: Any, condition: Any = None, when_true: Any = None, when_false: Any = None
) -> Any:
    """Conditionnelle en position d'expression.

    Les deux branches sont **paresseuses**, et c'est tout l'intérêt : la branche
    écartée peut lever sans conséquence, donc ``ifelse($.d == 0, 0, 100 / $.d)``
    est sûr. Avec des arguments évalués, elle aurait divisé par zéro avant même
    que la condition soit lue, et la fonction aurait été inutilisable là où on
    l'attend le plus — se protéger d'une donnée fautive.

    La condition se lit comme celle de ``filter`` / ``every`` (``coerce_bool``) :
    ``null``, ``0`` et ``""`` sont faux. Pas la lecture **stricte** de
    ``requirethat``, qui refuse tout ce qui n'est pas ``true`` : ici le cas
    courant est ``ifelse($.liste, …)`` ou ``ifelse($.flag, …)`` sur un flux où le
    booléen arrive en texte, et refuser l'aurait rendue pénible sans rien
    protéger — le résultat reste une valeur, pas une assertion.

    Branche absente : ``null``, comme un ``when`` sans ``default``.
    """
    taken = when_true if coerce_bool(condition) else when_false
    return None if taken is None else taken()
