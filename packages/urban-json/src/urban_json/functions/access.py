"""Accès **dynamique** à une valeur : ``get``, ``getpath``.

Sans contrepartie .NET, et c'était le trou le plus visible du moteur après
l'absence de conditionnelle : un chemin JSONPath est **littéral**. ``$.o[$.k]``
lève (« sélecteur de chemin non pris en charge »), et ``select`` n'accepte lui
aussi qu'un chemin écrit dans le template. Lire une configuration dont les clefs
*sont* des données — un dictionnaire de tarifs, une colonne nommée par le flux —
demandait donc ce détour :

    { "k:": $.k, "r": first(map(filter(entries($.o), $.key == k:), $.value)) }

quatre fonctions et une variable pour un accès par clef. ``get($.o, $.k)`` dit
la même chose.

Accepter une clef dynamique **dans la grammaire** (``$.o[$.k]``) demanderait de
modifier la grammaire ANTLR, donc ``java``, absent du conteneur ; une fonction
obtient le même résultat sans toucher au parser.

Convention de la famille des objets : une source qui n'est ni objet ni tableau
rend ``null``, comme une clef absente. Pour **exiger** la valeur, le refus
existe déjà et se lit mieux : ``require(get($.o, $.k), "tarif inconnu")``.
"""

from __future__ import annotations

from typing import Any

from ._helpers import is_number, to_text

# Même lecture d'un pas de chemin que `setpath` / `unsetpath` : indices de
# tableau compris, séparateur réglable. Importés plutôt que recopiés — deux
# copies de cette convention finiraient par diverger, et le lecteur n'aurait
# aucun moyen de savoir laquelle fait foi (cf. la leçon de `to_text`).
from .deep import _child, _separator
from .registry import jslt_function


@jslt_function(
    "get",
    description="Valeur d'une clef d'objet ou d'un indice de tableau calculés (null si absente)",
    description_en="Value of a computed object key or array index (null when absent)",
)
def execute_get(ctx: Any, token: Any = None, key: Any = None) -> Any:
    """Accès par clef **calculée**, ce que le chemin ne sait pas faire.

    Pas de 3e argument de repli : ``get($.o, $.k) ?? "inconnu"`` le dit déjà, et
    un repli en argument serait évalué même quand la clef existe.

    Un indice négatif compte depuis la fin (``get($.l, -1)`` = dernier), comme
    ``slice`` et ``substring`` ; hors bornes rend ``null`` plutôt que de lever,
    pour la même raison qu'eux — un template transforme des données qu'il n'a pas
    choisies.
    """
    if isinstance(token, dict):
        return token.get(to_text(key))
    if isinstance(token, list):
        return _at(token, key)
    return None


def _at(source: list, key: Any) -> Any:
    """Indice d'un tableau, négatif depuis la fin ; ``None`` si ce n'en est pas un."""
    if isinstance(key, bool) or not is_number(key):
        # Un tableau s'indexe par un nombre ; une clef textuelle n'y désigne
        # rien, donc « absent » — et non une erreur, cf. la convention ci-dessus.
        return None
    index = int(key)
    if index < 0:
        index += len(source)
    return source[index] if 0 <= index < len(source) else None


@jslt_function(
    "getpath",
    description="Valeur au bout d'un chemin pointé calculé (null si une étape manque)",
    description_en="Value at the end of a computed dotted path (null when a step is missing)",
)
def execute_getpath(
    ctx: Any, token: Any = None, path: Any = None, separator: Any = None
) -> Any:
    """Réciproque de ``setpath``, qui n'en avait pas.

    Le chemin est un **texte**, donc calculable : ``getpath($.o, $.champ)`` lit
    un chemin venu des données, là où ``$.a.b`` est figé dans le template. Les
    étapes se lisent comme celles de ``setpath`` (indices de tableau compris) et
    le séparateur est le même, réglable par le 3e argument.

    Une étape manquante rend ``null`` et n'interrompt rien : c'est la sémantique
    d'un chemin — ``$.a.b`` sur un document sans ``a`` rend ``null`` aussi, et
    ``??`` fournit le repli.
    """
    if not isinstance(token, (dict, list)):
        return None
    current: Any = token
    for step in to_text(path).split(_separator(separator)):
        if not isinstance(current, (dict, list)):
            return None
        current = _child(current, step)
    return current
