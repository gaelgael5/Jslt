"""Pliage Unicode : ``normalize``, ``deaccent``, ``foldtext``, ``slugify``.

Séparé de :mod:`.text` (qui édite une chaîne) parce que c'est un autre métier :
ici on **rapproche** deux écritures d'un même texte pour les comparer, les trier
ou en faire un identifiant. Aucune de ces fonctions ne connaît de collation
locale — ICU n'est pas une dépendance du cœur ; le pliage donne un ordre humain
pour les langues à diacritiques latins, et c'est dit dans la documentation.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any

from urban_json.errors import JsltError

from ._helpers import string_result, to_text
from .registry import jslt_function

# --- Unicode : normalisation, dépouillement, pliage --------------------------

_FORMS = {"C": "NFC", "D": "NFD", "KC": "NFKC", "KD": "NFKD"}


@jslt_function(
    "normalize", description="Normalise une chaîne Unicode : forme C (défaut), D, KC ou KD",
    description_en="Normalizes a Unicode string: form C (default), D, KC or KD"
)
def execute_normalize(ctx: Any, token: Any = None, form: Any = None) -> Any:
    # String.Normalize() .NET = forme C par défaut ; les trois autres formes sont
    # une extension, sans quoi la forme décomposée serait inatteignable.
    name = "C" if form is None else to_text(form).strip().upper()
    name = name.removeprefix("NF")
    if name not in _FORMS:
        raise JsltError(
            f"forme Unicode inconnue : {to_text(form)!r} (attendu : {', '.join(_FORMS)})"
        )
    return string_result(token, lambda s: unicodedata.normalize(_FORMS[name], s))


def _deaccent(value: str) -> str:
    # Décomposer, jeter les marques combinantes, recomposer : « é » -> « e ».
    # Une table de remplacement caractère par caractère raterait les écritures
    # déjà décomposées, fréquentes dans les exports macOS.
    decomposed = unicodedata.normalize("NFD", value)
    return unicodedata.normalize(
        "NFC", "".join(c for c in decomposed if unicodedata.category(c) != "Mn")
    )


@jslt_function(
    "deaccent", description="Retire les diacritiques (accents, cédilles) sans toucher à la casse",
    description_en="Removes diacritics (accents, cedillas) without touching the case"
)
def execute_deaccent(ctx: Any, token: Any = None) -> Any:
    return string_result(token, _deaccent)


_FOLDS = ("case", "accents")


@jslt_function(
    "foldtext",
    description=(
        "Clef de comparaison d'un texte : minuscules sans accents par défaut, "
        "ou seulement case / accents"
    ),
    description_en="Comparison key for a text: lowercase without accents by default, or case / accents only",
)
def execute_foldtext(ctx: Any, token: Any = None, options: Any = None) -> Any:
    """Rend une forme repliée, à comparer ou à trier.

    Plutôt qu'un opérateur de comparaison « insensible à la casse et aux
    accents », qui aurait dédoublé la sémantique de ``==`` : on replie les deux
    côtés et on compare normalement. La même clef sert à trier (``sort`` ne
    connaît pas les collations locales).
    """
    requested = [p for p in re.split(r"[,\s+]+", to_text(options).strip().lower()) if p]
    unknown = [p for p in requested if p not in _FOLDS]
    if unknown:
        raise JsltError(
            f"option de pliage inconnue : {unknown[0]!r} (attendu : {', '.join(_FOLDS)})"
        )
    wanted = requested or list(_FOLDS)  # sans option : tout replier

    def fold(value: str) -> str:
        if "accents" in wanted:
            value = _deaccent(value)
        return value.lower() if "case" in wanted else value

    return string_result(token, fold)


_SLUG_DROP = re.compile(r"[^a-z0-9]+")


@jslt_function(
    "slugify",
    description="Transforme un texte en identifiant d'URL : sans accent, en minuscules, mots joints par un tiret",
    description_en="Turns a text into a URL identifier: no accents, lower case, words joined by a dash",
)
def execute_slugify(ctx: Any, token: Any = None, separator: Any = None) -> Any:
    """Identifiant lisible depuis un libellé quelconque.

    S'écrivait en chaînant `deaccent`, `lower`, une regex et deux `trim` — assez
    long pour qu'on le fasse à peu près, et chaque template à peu près
    différemment.
    """
    joiner = "-" if separator is None else to_text(separator)

    def slug(value: str) -> str:
        return _SLUG_DROP.sub(joiner, _deaccent(value).lower()).strip(joiner or None)

    return string_result(token, slug)
