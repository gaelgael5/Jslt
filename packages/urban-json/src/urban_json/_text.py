"""La mise en texte d'une valeur jslt — **une seule** dans tout le moteur.

Module feuille (il n'importe que la bibliothèque standard) pour que les deux
côtés qui en ont besoin puissent s'en servir sans cycle d'import : les fonctions
(:mod:`urban_json.functions._helpers`) et les opérateurs
(:mod:`urban_json.runtime.operators`).

Il existe parce que la duplication a coûté deux fois le même défaut : chaque
copie rendait ``str(valeur)`` pour un tableau ou un objet, c'est-à-dire la
représentation **Python** (guillemets simples compris), qui ressortait telle
quelle dans le JSON produit. La première copie a été corrigée en 0.6.0, la
seconde — celle de ``"a" + $.liste`` — lui a survécu.
"""

from __future__ import annotations

import json
from typing import Any


def to_text(value: Any) -> str:
    """Texte d'une valeur, façon ``token.ToString()`` côté Newtonsoft.

    ``null`` rend la chaîne vide et les booléens gardent leur capitale .NET
    (``True`` / ``False``) ; un tableau ou un objet rend son **JSON compact**.
    """
    if value is None:
        return ""
    if value is True:
        return "True"
    if value is False:
        return "False"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)
