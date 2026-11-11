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
from typing import Any

from urban_json.errors import JsltError

from ._helpers import coerce_number, string_result, to_text
from .ordering import order_key
from .registry import jslt_function


@jslt_function("upper", description="Texte en majuscules (null reste null, une non-chaîne donne false)", description_en="Text in upper case (null stays null, a non-string gives false)")
def execute_upper(ctx: Any, token: Any = None) -> Any:
    return string_result(token, str.upper)


@jslt_function("lower", description="Texte en minuscules (null reste null, une non-chaîne donne false)", description_en="Text in lower case (null stays null, a non-string gives false)")
def execute_lower(ctx: Any, token: Any = None) -> Any:
    return string_result(token, str.lower)


@jslt_function("trim", description="Retire les espaces en début et fin, ou les caractères de txt s'il est donné", description_en="Removes the spaces at both ends, or the characters of txt when it is given")
def execute_trim(ctx: Any, token: Any = None, txt: str | None = None) -> Any:
    return string_result(token, lambda s: s.strip(txt) if txt else s.strip())


@jslt_function("split", description="Découpe un texte en tableau sur le premier caractère de charset (séparateur entier : splitstring)", description_en="Cuts a text into an array on the first character of charset (whole separator: splitstring)")
def execute_split(ctx: Any, token: Any = None, charset: str = "") -> Any:
    if token is None:
        return None
    if isinstance(token, str):
        return token.split(charset[0]) if charset else [token]
    return []


@jslt_function("startswith", description="Vrai si le texte commence par txt", description_en="True when the text starts with txt")
def execute_startswith(ctx: Any, token: Any = None, txt: str = "") -> Any:
    return string_result(token, lambda s: s.startswith(txt))


@jslt_function("endswith", description="Vrai si le texte se termine par txt", description_en="True when the text ends with txt")
def execute_endswith(ctx: Any, token: Any = None, txt: str = "") -> Any:
    return string_result(token, lambda s: s.endswith(txt))


@jslt_function("stringcontains", description="Vrai si le texte contient contain_str", description_en="True when the text holds contain_str")
def execute_stringcontains(ctx: Any, token: Any = None, contain_str: str = "") -> Any:
    return string_result(token, lambda s: contain_str in s)


@jslt_function(
    "indexof",
    description=(
        "Position (à partir de 0) de la première occurrence dans un texte ou un "
        "tableau, -1 si absent ; start cherche à partir de cette position"
    ),
    description_en=(
        "Position (from 0) of the first occurrence in a text or an array, -1 when absent; "
        "start searches from that position"
    ),
)
def execute_indexof(ctx: Any, token: Any = None, txt: Any = "", start: Any = 0) -> Any:
    # `start` cherche l'occurrence SUIVANTE : sans lui, parcourir toutes les
    # occurrences demandait de découper le texte à chaque tour.
    first = int(coerce_number(start))
    if isinstance(token, list):
        return _position(token, txt, last=False, start=first)
    return string_result(token, lambda s: s.find(to_text(txt), first))  # -1 si absent


@jslt_function(
    "lastindexof",
    description=(
        "Position (à partir de 0) de la dernière occurrence dans un texte ou un "
        "tableau, -1 si absent"
    ),
    description_en="Position (from 0) of the last occurrence in a text or an array, -1 when absent",
)
def execute_lastindexof(ctx: Any, token: Any = None, txt: Any = "") -> Any:
    if isinstance(token, list):
        return _position(token, txt, last=True)
    return string_result(token, lambda s: s.rfind(to_text(txt)))


def _position(source: list, value: Any, last: bool, start: int = 0) -> int:
    """Position d'une valeur dans un tableau, -1 si absente.

    Égalité **structurelle** (la clef d'ordre), comme les opérations
    ensemblistes : chercher `2` ne doit pas trouver `"2"`, sinon la position
    rendue dépendrait du typage du flux. `contains`, lui, garde l'égalité `==`
    du langage pour rester fidèle au .NET — l'écart est volontaire.
    """
    marker = order_key(value)
    first = start if start >= 0 else max(0, len(source) + start)
    positions = range(len(source) - 1, first - 1, -1) if last else range(first, len(source))
    for index in positions:
        if order_key(source[index]) == marker:
            return index
    return -1


@jslt_function("padleft", description="Complète le texte à gauche jusqu'à length avec le 1er caractère de charset (espace par défaut)", description_en="Pads the text on the left up to length with the 1st character of charset (space by default)")
def execute_padleft(ctx: Any, token: Any = None, length: int = 0, charset: str = " ") -> Any:
    fill = charset[0] if charset else " "
    return string_result(token, lambda s: s.rjust(length, fill))


@jslt_function("padright", description="Complète le texte à droite jusqu'à length avec le 1er caractère de charset (espace par défaut)", description_en="Pads the text on the right up to length with the 1st character of charset (space by default)")
def execute_padright(ctx: Any, token: Any = None, length: int = 0, charset: str = " ") -> Any:
    fill = charset[0] if charset else " "
    return string_result(token, lambda s: s.ljust(length, fill))


# Deux noms, une seule implémentation. `stringlenght` porte une faute de frappe
# d'origine : la retirer casserait les templates écrits avec, la garder seule
# obligeait à écrire une faute pour appeler la fonction. Les deux décorateurs
# enregistrent la **même** callable : les deux noms ne peuvent donc pas diverger.
@jslt_function("stringlength", description="Nombre de caractères d'un texte (0 pour null ou une non-chaîne)", description_en="Number of characters of a text (0 for null or a non-string)")
@jslt_function("stringlenght", description="Nombre de caractères d'un texte — orthographe d'origine, fautive, conservée : voir stringlength", description_en="Number of characters of a text — original, misspelled name kept: see stringlength")
def execute_stringlenght(ctx: Any, token: Any = None) -> int:
    # Convention .NET : null -> 0 ; chaîne -> longueur ; autre -> 0.
    return len(token) if isinstance(token, str) else 0

# --- Extraction et remplacement ----------------------------------------------


@jslt_function(
    "substring",
    description=(
        "Extrait length caractères à partir de start (start négatif = depuis la fin, "
        "length absente = jusqu'au bout)"
    ),
    description_en="Extracts length characters from start (negative start = from the end, length absent = to the end)",
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


@jslt_function("replace", description="Remplace toutes les occurrences de search par replacement", description_en="Replaces every occurrence of search with replacement")
def execute_replace(
    ctx: Any, token: Any = None, search: Any = None, replacement: Any = None
) -> Any:
    needle = to_text(search)
    if not needle:
        # str.replace("") insérerait le remplacement entre chaque caractère :
        # personne n'écrit cela volontairement, on rend le texte intact.
        return string_result(token, lambda s: s)
    return string_result(token, lambda s: s.replace(needle, to_text(replacement)))


@jslt_function("trimstart", description="Retire les espaces en début, ou les caractères de txt", description_en="Removes the leading spaces, or the characters of txt")
def execute_trimstart(ctx: Any, token: Any = None, txt: Any = None) -> Any:
    chars = None if txt is None else to_text(txt)
    return string_result(token, lambda s: s.lstrip(chars) if chars else s.lstrip())


@jslt_function("trimend", description="Retire les espaces en fin, ou les caractères de txt", description_en="Removes the trailing spaces, or the characters of txt")
def execute_trimend(ctx: Any, token: Any = None, txt: Any = None) -> Any:
    chars = None if txt is None else to_text(txt)
    return string_result(token, lambda s: s.rstrip(chars) if chars else s.rstrip())


@jslt_function("repeat", description="Répète le texte count fois (0 ou négatif : chaîne vide)", description_en="Repeats the text count times (0 or negative: empty string)")
def execute_repeat(ctx: Any, token: Any = None, count: Any = 0) -> Any:
    times = max(int(coerce_number(count)), 0)
    return string_result(token, lambda s: s * times)


_WORD_START = re.compile(r"(?<![^\W\d_])[^\W\d_]", re.UNICODE)


@jslt_function(
    "titlecase",
    description="Met en majuscule la première lettre de chaque mot, sans toucher au reste",
    description_en="Upper-cases the first letter of every word, leaving the rest alone",
)
def execute_titlecase(ctx: Any, token: Any = None) -> Any:
    """Majuscule initiale de chaque mot, le reste intact.

    `str.title()` abaisserait les lettres suivantes et rendrait « Mcdonald »
    d'un « McDonald » déjà correct : sur des noms propres venus de données
    réelles, c'est une dégradation, pas une mise en forme.
    """
    return string_result(token, lambda s: _WORD_START.sub(lambda m: m.group(0).upper(), s))


@jslt_function(
    "splitstring",
    description=(
        "Découpe un texte sur un séparateur complet (plusieurs caractères), "
        "au plus limit fois"
    ),
    description_en="Cuts a text on a whole separator (several characters), at most limit times",
)
def execute_splitstring(ctx: Any, token: Any = None, separator: Any = None, limit: Any = None) -> Any:
    """Découpe sur le séparateur **entier**.

    `split` ne retient que le premier caractère du séparateur, par fidélité au
    .NET : `split($.t, ", ")` coupe sur la virgule et laisse les espaces. C'est
    silencieux et faux pour qui écrit un séparateur de deux caractères, d'où
    cette fonction plutôt qu'un changement de `split`, qui casserait les
    templates portés.
    """
    cuts = -1 if limit is None else int(coerce_number(limit))
    text = to_text(separator)
    if not text:
        # Découper sur « rien » rendrait la liste des caractères : personne ne
        # l'écrit volontairement.
        return string_result(token, lambda s: [s])
    return string_result(token, lambda s: s.split(text, cuts))


@jslt_function(
    "shorten",
    description="Raccourcit un texte à length caractères au plus, suffixe compris (… par défaut)",
    description_en="Shortens a text to length characters at most, suffix included (… by default)",
)
def execute_shorten(ctx: Any, token: Any = None, length: Any = None, suffix: Any = None) -> Any:
    """Raccourcit avec une ellipse, suffixe **compris** dans la longueur.

    Le nom n'est pas `truncate` : il est déjà pris par la troncature numérique
    du .NET. Le suffixe compte dans la longueur demandée, sinon « 8 caractères
    maximum » en rendrait 9 et déborderait la colonne qu'on voulait tenir.
    """
    size = 0 if length is None else int(coerce_number(length))
    marker = "…" if suffix is None else to_text(suffix)
    if size <= len(marker):
        raise JsltError(
            f"longueur insuffisante pour shorten : {length!r} (doit dépasser le "
            f"suffixe {marker!r})"
        )

    def cut(value: str) -> str:
        if len(value) <= size:
            return value
        kept = value[: size - len(marker)]
        # Si la coupe tombe au milieu d'un mot, on remonte au dernier espace :
        # « Paris L… » donne à lire un mot qui n'existe pas. Sans espace dans la
        # fenêtre (un identifiant, un mot très long), on coupe net plutôt que de
        # tout perdre.
        if value[len(kept) : len(kept) + 1].strip() and " " in kept.strip():
            kept = kept[: kept.rstrip().rfind(" ")]
        return kept.rstrip() + marker

    return string_result(token, cut)
