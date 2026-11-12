"""Découper et retoucher un texte : ``chars``, ``lines``, ``words``,
``removeprefix``, ``removesuffix``, ``capitalize``.

Sans contrepartie .NET. Trois de ces besoins avaient une réponse qui **semblait**
fonctionner : ``splitstring($.t, "")`` rend le texte entier, ``trimstart`` retire
un **jeu de caractères** et non un préfixe (sur « bacab », ``trimstart(t, "ab")``
rend « cab » alors que le préfixe « ab » n'y est pas), et ``titlecase`` met
**toutes** les initiales.

Convention de la famille, celle de ``upper`` : ``null`` reste ``null``, une
valeur qui n'est pas une chaîne donne ``false``.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any

from ._helpers import string_result, to_text
from .registry import jslt_function

#: Les trois fins de ligne, la plus longue d'abord (sinon `\r\n` compte double).
_LINES = re.compile(r"\r\n|\n|\r")


def _graphemes(value: str) -> list[str]:
    """Caractères **perçus** : une base plus ses marques combinantes.

    Même découpe que ``reverse`` sur un texte — découper par point de code
    collerait un accent sur la lettre voisine.
    """
    clusters: list[str] = []
    for char in value:
        if clusters and unicodedata.combining(char):
            clusters[-1] += char
        else:
            clusters.append(char)
    return clusters


@jslt_function(
    "chars",
    description="Découpe un texte en tableau de caractères (par graphème)",
    description_en="Splits a text into an array of characters (by grapheme)",
)
def execute_chars(ctx: Any, token: Any = None) -> Any:
    return string_result(token, _graphemes)


@jslt_function(
    "lines",
    description="Découpe un texte en lignes (\\n, \\r\\n ou \\r), lignes vides comprises",
    description_en="Splits a text into lines (\\n, \\r\\n or \\r), empty lines included",
)
def execute_lines(ctx: Any, token: Any = None) -> Any:
    """Les lignes vides sont gardées : une ligne vide est une ligne, et la
    retirer décalerait toute numérotation construite dessus."""
    return string_result(token, lambda text: _LINES.split(text))


@jslt_function(
    "words",
    description="Découpe un texte en mots sur les espaces (les vides sont ignorés)",
    description_en="Splits a text into words on whitespace (empty ones are dropped)",
)
def execute_words(ctx: Any, token: Any = None) -> Any:
    return string_result(token, lambda text: text.split())


@jslt_function(
    "removeprefix",
    description="Retire un préfixe **entier** s'il est présent, sinon rend le texte inchangé",
    description_en="Removes a whole prefix when present, otherwise returns the text unchanged",
)
def execute_removeprefix(ctx: Any, token: Any = None, prefix: Any = "") -> Any:
    """À ne pas confondre avec ``trimstart``, qui retire des **caractères**."""
    affix = to_text(prefix)
    return string_result(token, lambda text: text[len(affix):] if affix and text.startswith(affix) else text)


@jslt_function(
    "removesuffix",
    description="Retire un suffixe **entier** s'il est présent, sinon rend le texte inchangé",
    description_en="Removes a whole suffix when present, otherwise returns the text unchanged",
)
def execute_removesuffix(ctx: Any, token: Any = None, suffix: Any = "") -> Any:
    affix = to_text(suffix)
    return string_result(token, lambda text: text[: -len(affix)] if affix and text.endswith(affix) else text)


@jslt_function(
    "capitalize",
    description="Met en majuscule la première lettre seulement, sans toucher au reste",
    description_en="Upper-cases the first letter only, leaving the rest untouched",
)
def execute_capitalize(ctx: Any, token: Any = None) -> Any:
    """``titlecase`` met **toutes** les initiales ; ici une seule, et le reste
    est laissé tel quel (un sigle en capitales le reste)."""
    return string_result(token, lambda text: text[:1].upper() + text[1:])
