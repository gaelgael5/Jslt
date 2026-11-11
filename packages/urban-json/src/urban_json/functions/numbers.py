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

``tohex`` / ``fromhex`` sont les cas particuliers de ``tobase`` / ``frombase``
qu'on écrit le plus souvent ; ils restent pour cela, et doivent concorder.
"""

from __future__ import annotations

import math
import re
from typing import Any

from urban_json.errors import JsltError

from ._helpers import coerce_number, is_number, number_result, to_text
from .formatting import _culture
from .registry import jslt_function

# Tout ce qui n'est ni chiffre, ni signe, ni séparateur : symbole monétaire,
# pourcentage, espace insécable des milliers français…
_NOT_NUMERIC = re.compile(r"[^\d+\-.,\s  ]")


@jslt_function(
    "parsenumber",
    description="Lit un nombre écrit en texte selon une culture (1 234,56 en fr-FR)",
    description_en="Reads a number written as text according to a culture (1 234,56 in fr-FR)",
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


@jslt_function("sign", description="Signe d'un nombre : -1, 0 ou 1", description_en="Sign of a number: -1, 0 or 1")
def execute_sign(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: (n > 0) - (n < 0))


@jslt_function("clamp", description="Ramène un nombre dans l'intervalle [lower, upper]", description_en="Brings a number back into the [lower, upper] range")
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


@jslt_function("gcd", description="Plus grand commun diviseur de deux entiers", description_en="Greatest common divisor of two integers")
def execute_gcd(ctx: Any, left: Any = None, right: Any = None) -> Any:
    return math.gcd(abs(_whole(left, "gcd")), abs(_whole(right, "gcd")))


@jslt_function("shiftleft", description="Décale les bits d'un entier vers la gauche (multiplie par 2^bits)", description_en="Shifts the bits of an integer to the left (multiplies by 2^bits)")
def execute_shiftleft(ctx: Any, token: Any = None, bits: Any = 0) -> Any:
    return _whole(token, "shiftleft") << _whole(bits, "shiftleft")


@jslt_function("shiftright", description="Décale les bits d'un entier vers la droite (divise par 2^bits)", description_en="Shifts the bits of an integer to the right (divides by 2^bits)")
def execute_shiftright(ctx: Any, token: Any = None, bits: Any = 0) -> Any:
    return _whole(token, "shiftright") >> _whole(bits, "shiftright")


@jslt_function(
    "tohex",
    description="Écrit un entier en hexadécimal minuscule, complété à width chiffres",
    description_en="Writes an integer in lower-case hexadecimal, padded to width digits",
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


@jslt_function("fromhex", description="Lit un entier écrit en hexadécimal (avec ou sans préfixe 0x)", description_en="Reads an integer written in hexadecimal (with or without the 0x prefix)")
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


@jslt_function("log", description="Logarithme d'un nombre dans la base donnée", description_en="Logarithm of a number in the given base")
def execute_log(ctx: Any, token: Any = None, base: Any = None) -> Any:
    """Logarithme à base libre, là où ``logarithm`` est fixé à e (et ses
    variantes à 10 et 2)."""
    if not is_number(base) or base <= 0 or base == 1:
        raise JsltError(f"base de logarithme invalide : {base!r} (attendu : > 0 et ≠ 1)")
    if not is_number(token):
        return None
    if token <= 0:
        raise JsltError(f"logarithme d'une valeur non positive : {token!r}")
    # Les deux bases usuelles passent par leur fonction dédiée : `math.log(x, b)`
    # divise deux logarithmes et rend 2.9999999999999996 pour log10(1000), ce
    # qui ressort tel quel dans le JSON produit.
    if base == 10:
        return math.log10(token)
    if base == 2:
        return math.log2(token)
    return math.log(token, base)


@jslt_function("isfinite", description="Vrai si la valeur est un nombre fini (ni infini, ni NaN)", description_en="True when the value is a finite number (neither infinite nor NaN)")
def execute_isfinite(ctx: Any, token: Any = None) -> bool:
    """Un calcul peut produire l'infini (débordement d'un produit) alors que
    JSON ne sait pas l'écrire : sans ce test, la valeur se propage et ressort en
    ``Infinity``, que la plupart des lecteurs JSON refusent."""
    return is_number(token) and math.isfinite(token)


@jslt_function("isnan", description="Vrai si la valeur est le résultat indéfini d'un calcul (NaN)", description_en="True when the value is the undefined result of a computation (NaN)")
def execute_isnan(ctx: Any, token: Any = None) -> bool:
    return is_number(token) and math.isnan(token)


_DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def _base(base: Any) -> int:
    value = int(coerce_number(base)) if is_number(base) else 0
    if not 2 <= value <= 36:
        raise JsltError(f"base invalide : {base!r} (attendu : de 2 à 36)")
    return value


@jslt_function(
    "tobase",
    description="Écrit un entier dans une base de 2 à 36, complété à width chiffres",
    description_en="Writes an integer in a base from 2 to 36, padded to width digits",
)
def execute_tobase(ctx: Any, token: Any = None, base: Any = None, width: Any = 0) -> Any:
    radix = _base(base)
    if not is_number(token):
        return None
    value = _whole(token, "tobase")
    size = _whole(width, "tobase") if width else 0
    rest, digits = abs(value), ""
    while rest:
        rest, digit = divmod(rest, radix)
        digits = _DIGITS[digit] + digits
    digits = (digits or "0").rjust(size, "0")
    # Signe devant les chiffres, comme `tohex` : un entier JSON n'a pas de
    # largeur, donc pas de complément à deux naturel.
    return f"-{digits}" if value < 0 else digits


@jslt_function("frombase", description="Lit un entier écrit dans une base de 2 à 36", description_en="Reads an integer written in a base from 2 to 36")
def execute_frombase(ctx: Any, token: Any = None, base: Any = None) -> Any:
    radix = _base(base)
    if token is None:
        return None
    text = to_text(token).strip().lower()
    negative = text.startswith("-")
    try:
        value = int(text.lstrip("-"), radix)
    except ValueError as exc:
        raise JsltError(f"illisible en base {radix} : {token!r}") from exc
    return -value if negative else value
