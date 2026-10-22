"""Fonctions de chaîne intégrées (port des ``Services.strings`` .NET).

Convention : ``None`` -> ``None``, chaîne -> résultat, autre valeur -> ``False``
(sauf ``stringlenght`` qui suit sa propre convention .NET).
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any

from urban_json.errors import JsltError

from ._helpers import string_result, to_text
from .registry import jslt_function


@jslt_function("upper")
def execute_upper(ctx: Any, token: Any = None) -> Any:
    return string_result(token, str.upper)


@jslt_function("lower")
def execute_lower(ctx: Any, token: Any = None) -> Any:
    return string_result(token, str.lower)


@jslt_function("trim")
def execute_trim(ctx: Any, token: Any = None, txt: str | None = None) -> Any:
    return string_result(token, lambda s: s.strip(txt) if txt else s.strip())


@jslt_function("split")
def execute_split(ctx: Any, token: Any = None, charset: str = "") -> Any:
    if token is None:
        return None
    if isinstance(token, str):
        return token.split(charset[0]) if charset else [token]
    return []


@jslt_function("startswith")
def execute_startswith(ctx: Any, token: Any = None, txt: str = "") -> Any:
    return string_result(token, lambda s: s.startswith(txt))


@jslt_function("endswith")
def execute_endswith(ctx: Any, token: Any = None, txt: str = "") -> Any:
    return string_result(token, lambda s: s.endswith(txt))


@jslt_function("stringcontains")
def execute_stringcontains(ctx: Any, token: Any = None, contain_str: str = "") -> Any:
    return string_result(token, lambda s: contain_str in s)


@jslt_function("indexof")
def execute_indexof(ctx: Any, token: Any = None, txt: str = "") -> Any:
    return string_result(token, lambda s: s.find(txt))  # -1 si absent


@jslt_function("lastindexof")
def execute_lastindexof(ctx: Any, token: Any = None, txt: str = "") -> Any:
    return string_result(token, lambda s: s.rfind(txt))


@jslt_function("padleft")
def execute_padleft(ctx: Any, token: Any = None, length: int = 0, charset: str = " ") -> Any:
    fill = charset[0] if charset else " "
    return string_result(token, lambda s: s.rjust(length, fill))


@jslt_function("padright")
def execute_padright(ctx: Any, token: Any = None, length: int = 0, charset: str = " ") -> Any:
    fill = charset[0] if charset else " "
    return string_result(token, lambda s: s.ljust(length, fill))


@jslt_function("stringlenght")
def execute_stringlenght(ctx: Any, token: Any = None) -> int:
    # Convention .NET : null -> 0 ; chaîne -> longueur ; autre -> 0.
    return len(token) if isinstance(token, str) else 0


@jslt_function("normalize", description="Normalise une chaîne Unicode (forme C : caractères composés)")
def execute_normalize(ctx: Any, token: Any = None) -> Any:
    # String.Normalize() .NET = forme C par défaut.
    return string_result(token, lambda s: unicodedata.normalize("NFC", s))


# --- Expressions régulières (port de regexismatch / regexmatches .NET) ---------
# Dialecte : celui du module ``re`` de Python, proche de .NET pour l'usage courant
# (classes, quantificateurs, ancres, lookarounds). Seul écart traduit : le groupe
# nommé .NET ``(?<nom>…)``, que ``re`` refuse (il n'accepte que ``(?P<nom>…)``) —
# sans cette traduction, un template écrit pour le .NET lèverait une erreur.
_DOTNET_NAMED_GROUP = re.compile(r"(?<!\\)\(\?<(?![=!])")


def _regex_subject(token: Any) -> str | None:
    """Texte soumis à la regex : un scalaire converti comme en .NET (nombre en
    culture invariante, booléen ``True``/``False``) ; ``None`` pour null, objet ou
    tableau. Le .NET levait sur null (NullReferenceException) : on rend ``null``,
    comme les autres fonctions de chaîne."""
    if token is None or isinstance(token, (dict, list)):
        return None
    return to_text(token)


def _compile(pattern: Any) -> re.Pattern[str]:
    try:
        return re.compile(_DOTNET_NAMED_GROUP.sub("(?P<", to_text(pattern)))
    except re.error as exc:
        raise JsltError(f"motif regex invalide {pattern!r} : {exc}") from exc


@jslt_function("regexismatch", description="Vrai si le texte contient une correspondance du motif regex")
def execute_regexismatch(ctx: Any, token: Any = None, pattern: str = "") -> Any:
    subject = _regex_subject(token)
    if subject is None:
        return None
    # search, pas match : Regex.IsMatch .NET n'est pas ancré au début.
    return _compile(pattern).search(subject) is not None


@jslt_function("regexmatches", description="Liste des correspondances du motif regex dans le texte")
def execute_regexmatches(ctx: Any, token: Any = None, pattern: str = "") -> Any:
    subject = _regex_subject(token)
    if subject is None:
        return None
    # group(0) = correspondance complète (Match.Value .NET) ; findall renverrait
    # les groupes capturés dès qu'il y en a.
    return [m.group(0) for m in _compile(pattern).finditer(subject)]
