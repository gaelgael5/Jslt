"""Fonctions de chaîne intégrées (port des ``Services.strings`` .NET, étendu).

Convention : ``None`` -> ``None``, chaîne -> résultat, autre valeur -> ``False``
(sauf ``stringlenght``, qui suit sa propre convention .NET). Les expressions
régulières vivent dans :mod:`.regexes` — elles suivent une autre convention.

Au-delà du .NET : extraction (``substring``), remplacement (``replace``),
rognage dirigé (``trimstart`` / ``trimend``), ``repeat``, ``titlecase``, et le
pliage Unicode (``deaccent``, ``foldtext``, formes de ``normalize``).
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any

from urban_json.errors import JsltError

from ._helpers import coerce_number, string_result, to_text
from .registry import jslt_function


@jslt_function("upper", description="Texte en majuscules (null reste null, une non-chaîne donne false)")
def execute_upper(ctx: Any, token: Any = None) -> Any:
    return string_result(token, str.upper)


@jslt_function("lower", description="Texte en minuscules (null reste null, une non-chaîne donne false)")
def execute_lower(ctx: Any, token: Any = None) -> Any:
    return string_result(token, str.lower)


@jslt_function("trim", description="Retire les espaces en début et fin, ou les caractères de txt s'il est donné")
def execute_trim(ctx: Any, token: Any = None, txt: str | None = None) -> Any:
    return string_result(token, lambda s: s.strip(txt) if txt else s.strip())


@jslt_function("split", description="Découpe un texte en tableau sur le premier caractère de charset")
def execute_split(ctx: Any, token: Any = None, charset: str = "") -> Any:
    if token is None:
        return None
    if isinstance(token, str):
        return token.split(charset[0]) if charset else [token]
    return []


@jslt_function("startswith", description="Vrai si le texte commence par txt")
def execute_startswith(ctx: Any, token: Any = None, txt: str = "") -> Any:
    return string_result(token, lambda s: s.startswith(txt))


@jslt_function("endswith", description="Vrai si le texte se termine par txt")
def execute_endswith(ctx: Any, token: Any = None, txt: str = "") -> Any:
    return string_result(token, lambda s: s.endswith(txt))


@jslt_function("stringcontains", description="Vrai si le texte contient contain_str")
def execute_stringcontains(ctx: Any, token: Any = None, contain_str: str = "") -> Any:
    return string_result(token, lambda s: contain_str in s)


@jslt_function("indexof", description="Position (à partir de 0) de la première occurrence de txt, -1 si absent")
def execute_indexof(ctx: Any, token: Any = None, txt: str = "") -> Any:
    return string_result(token, lambda s: s.find(txt))  # -1 si absent


@jslt_function("lastindexof", description="Position (à partir de 0) de la dernière occurrence de txt, -1 si absent")
def execute_lastindexof(ctx: Any, token: Any = None, txt: str = "") -> Any:
    return string_result(token, lambda s: s.rfind(txt))


@jslt_function("padleft", description="Complète le texte à gauche jusqu'à length avec le 1er caractère de charset (espace par défaut)")
def execute_padleft(ctx: Any, token: Any = None, length: int = 0, charset: str = " ") -> Any:
    fill = charset[0] if charset else " "
    return string_result(token, lambda s: s.rjust(length, fill))


@jslt_function("padright", description="Complète le texte à droite jusqu'à length avec le 1er caractère de charset (espace par défaut)")
def execute_padright(ctx: Any, token: Any = None, length: int = 0, charset: str = " ") -> Any:
    fill = charset[0] if charset else " "
    return string_result(token, lambda s: s.ljust(length, fill))


@jslt_function("stringlenght", description="Nombre de caractères d'un texte (0 pour null ou une non-chaîne) — orthographe d'origine conservée")
def execute_stringlenght(ctx: Any, token: Any = None) -> int:
    # Convention .NET : null -> 0 ; chaîne -> longueur ; autre -> 0.
    return len(token) if isinstance(token, str) else 0

# --- Unicode : normalisation, dépouillement, pliage --------------------------

_FORMS = {"C": "NFC", "D": "NFD", "KC": "NFKC", "KD": "NFKD"}


@jslt_function(
    "normalize", description="Normalise une chaîne Unicode : forme C (défaut), D, KC ou KD"
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
    "deaccent", description="Retire les diacritiques (accents, cédilles) sans toucher à la casse"
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


# --- Extraction et remplacement ----------------------------------------------


@jslt_function(
    "substring",
    description=(
        "Extrait length caractères à partir de start (start négatif = depuis la fin, "
        "length absente = jusqu'au bout)"
    ),
)
def execute_substring(ctx: Any, token: Any = None, start: Any = 0, length: Any = None) -> Any:
    """Morceau de chaîne, sans lever sur des bornes trop larges.

    `Substring` en .NET jette dès que les bornes sortent de la chaîne ; ici un
    début hors bornes rend une chaîne vide et une longueur trop grande s'arrête
    au bout. Un template transforme des données qu'il ne choisit pas : tomber sur
    un champ plus court que prévu ne doit pas faire échouer la transformation
    entière. Une longueur **négative** lève, elle : c'est une faute d'écriture du
    template, pas une donnée surprenante.
    """
    begin = 0 if start is None else int(coerce_number(start))
    size = None if length is None else int(coerce_number(length))
    if size is not None and size < 0:
        raise JsltError(f"longueur négative interdite pour substring : {length!r}")

    def cut(value: str) -> str:
        first = max(len(value) + begin, 0) if begin < 0 else begin
        return value[first:] if size is None else value[first : first + size]

    return string_result(token, cut)


@jslt_function("replace", description="Remplace toutes les occurrences de search par replacement")
def execute_replace(
    ctx: Any, token: Any = None, search: Any = None, replacement: Any = None
) -> Any:
    needle = to_text(search)
    if not needle:
        # str.replace("") insérerait le remplacement entre chaque caractère :
        # personne n'écrit cela volontairement, on rend le texte intact.
        return string_result(token, lambda s: s)
    return string_result(token, lambda s: s.replace(needle, to_text(replacement)))


@jslt_function("trimstart", description="Retire les espaces en début, ou les caractères de txt")
def execute_trimstart(ctx: Any, token: Any = None, txt: Any = None) -> Any:
    chars = None if txt is None else to_text(txt)
    return string_result(token, lambda s: s.lstrip(chars) if chars else s.lstrip())


@jslt_function("trimend", description="Retire les espaces en fin, ou les caractères de txt")
def execute_trimend(ctx: Any, token: Any = None, txt: Any = None) -> Any:
    chars = None if txt is None else to_text(txt)
    return string_result(token, lambda s: s.rstrip(chars) if chars else s.rstrip())


@jslt_function("repeat", description="Répète le texte count fois (0 ou négatif : chaîne vide)")
def execute_repeat(ctx: Any, token: Any = None, count: Any = 0) -> Any:
    times = max(int(coerce_number(count)), 0)
    return string_result(token, lambda s: s * times)


_WORD_START = re.compile(r"(?<![^\W\d_])[^\W\d_]", re.UNICODE)


@jslt_function(
    "titlecase",
    description="Met en majuscule la première lettre de chaque mot, sans toucher au reste",
)
def execute_titlecase(ctx: Any, token: Any = None) -> Any:
    """Majuscule initiale de chaque mot, le reste intact.

    `str.title()` abaisserait les lettres suivantes et rendrait « Mcdonald »
    d'un « McDonald » déjà correct : sur des noms propres venus de données
    réelles, c'est une dégradation, pas une mise en forme.
    """
    return string_result(token, lambda s: _WORD_START.sub(lambda m: m.group(0).upper(), s))
