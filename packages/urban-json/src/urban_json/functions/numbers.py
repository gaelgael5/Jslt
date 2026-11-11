"""Lecture et manipulation de nombres : ``parsenumber``, ``sign``, ``clamp``,
``gcd``, ``shiftleft`` / ``shiftright``, ``tohex`` / ``fromhex``.

``parsenumber`` est le pendant de ``parsedate`` : le moteur savait écrire un
nombre selon une culture (``format($.v, "N2", "fr-FR")``) sans savoir le relire,
donc un flux où les montants arrivent en texte localisé n'était pas traitable.
Il réutilise les **mêmes** données de culture que ``format`` (:mod:`.formatting`),
pour que l'aller-retour soit fermé par construction.

Les décalages de bits sont des fonctions et non des opérateurs : ajouter
``<<`` / ``>>`` à la grammaire imposerait de régénérer le parser ANTLR, alors que
``&``, ``|`` et ``^`` existent déjà comme opérateurs.
"""

from __future__ import annotations

import math
import re
from typing import Any

from urban_json.errors import JsltError

from ._helpers import is_number, number_result, to_text
from .formatting import _culture
from .registry import jslt_function

# Tout ce qui n'est ni chiffre, ni signe, ni séparateur : symbole monétaire,
# pourcentage, espace insécable des milliers français…
_NOT_NUMERIC = re.compile(r"[^\d+\-.,\s  ]")


@jslt_function(
    "parsenumber",
    description="Lit un nombre écrit en texte selon une culture (1 234,56 en fr-FR)",
)
def execute_parsenumber(ctx: Any, token: Any = None, culture: Any = None) -> Any:
    """Texte -> nombre, selon les séparateurs de la culture.

    Un entier reste un entier (``"42"`` donne ``42``, pas ``42.0``), comme
    ``sum`` garde l'entier. Un texte illisible **lève** : rendre ``null``
    transformerait un montant corrompu en « pas de montant », et le total
    ensuite calculé serait faux sans que rien ne le signale.
    """
    if token is None:
        return None
    if is_number(token):
        return token
    if not isinstance(token, str):
        raise JsltError(f"parsenumber attend un texte, reçu : {token!r}")
    rules = _culture(culture)
    cleaned = _NOT_NUMERIC.sub("", token).strip()
    # L'ordre compte : on retire d'abord les séparateurs de milliers, sinon le
    # point de « 1.234,56 » (de-DE) serait pris pour une virgule décimale.
    cleaned = cleaned.replace(rules.group, "").replace(" ", "").replace(" ", "")
    cleaned = cleaned.replace(" ", "").replace(rules.decimal, ".")
    try:
        return int(cleaned)
    except ValueError:
        pass
    try:
        return float(cleaned)
    except ValueError as exc:
        raise JsltError(f"nombre illisible dans {token!r} (culture {culture!r})") from exc


@jslt_function("sign", description="Signe d'un nombre : -1, 0 ou 1")
def execute_sign(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: (n > 0) - (n < 0))


@jslt_function("clamp", description="Ramène un nombre dans l'intervalle [lower, upper]")
def execute_clamp(ctx: Any, token: Any = None, lower: Any = None, upper: Any = None) -> Any:
    if not is_number(lower) or not is_number(upper):
        raise JsltError(f"clamp attend deux bornes numériques, reçu : {lower!r}, {upper!r}")
    if lower > upper:
        # Bornes inversées : silencieusement corrigées, le résultat serait
        # plausible et faux ; c'est une faute d'écriture du template.
        raise JsltError(f"bornes inversées pour clamp : {lower!r} > {upper!r}")
    return number_result(token, lambda n: min(max(n, lower), upper))


def _whole(value: Any, name: str) -> int:
    if not is_number(value) or int(value) != value:
        raise JsltError(f"{name} attend un entier, reçu : {value!r}")
    return int(value)


@jslt_function("gcd", description="Plus grand commun diviseur de deux entiers")
def execute_gcd(ctx: Any, left: Any = None, right: Any = None) -> Any:
    return math.gcd(abs(_whole(left, "gcd")), abs(_whole(right, "gcd")))


@jslt_function("shiftleft", description="Décale les bits d'un entier vers la gauche (multiplie par 2^bits)")
def execute_shiftleft(ctx: Any, token: Any = None, bits: Any = 0) -> Any:
    return _whole(token, "shiftleft") << _whole(bits, "shiftleft")


@jslt_function("shiftright", description="Décale les bits d'un entier vers la droite (divise par 2^bits)")
def execute_shiftright(ctx: Any, token: Any = None, bits: Any = 0) -> Any:
    return _whole(token, "shiftright") >> _whole(bits, "shiftright")


@jslt_function(
    "tohex",
    description="Écrit un entier en hexadécimal minuscule, complété à width chiffres",
)
def execute_tohex(ctx: Any, token: Any = None, width: Any = 0) -> Any:
    if not is_number(token):
        return None
    value = _whole(token, "tohex")
    size = _whole(width, "tohex") if width else 0
    digits = format(abs(value), "x").rjust(size, "0")
    # Le signe devant les chiffres, pas de complément à deux : un entier JSON
    # n'a pas de largeur, donc pas de représentation signée naturelle.
    return f"-{digits}" if value < 0 else digits


@jslt_function("fromhex", description="Lit un entier écrit en hexadécimal (avec ou sans préfixe 0x)")
def execute_fromhex(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    text = to_text(token).strip().lower()
    negative = text.startswith("-")
    digits = text.lstrip("-").removeprefix("0x")
    try:
        value = int(digits, 16)
    except ValueError as exc:
        raise JsltError(f"hexadécimal illisible : {token!r}") from exc
    return -value if negative else value
