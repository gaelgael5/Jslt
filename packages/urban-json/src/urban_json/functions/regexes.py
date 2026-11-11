"""Expressions régulières : ``regexismatch``, ``regexmatches``, ``regexreplace``.

Dialecte : celui du module ``re`` de Python, proche de .NET pour l'usage courant
(classes, quantificateurs, ancres, lookarounds). Deux écarts sont **traduits**,
sans quoi un motif ou un remplacement écrit pour le .NET se comporterait
autrement : le groupe nommé ``(?<nom>…)`` et la syntaxe de substitution
``$1`` / ``${nom}`` / ``$&``.

Convention de la famille : un scalaire est converti en texte (``42`` devient
``"42"``, comme en .NET) ; ``null``, un objet ou un tableau donnent ``null``.
C'est volontairement **différent** des fonctions de chaîne de :mod:`.text`, qui
rendent ``false`` sur une non-chaîne — chercher un motif dans un nombre a un
sens, le mettre en majuscules non.
"""

from __future__ import annotations

import re
from typing import Any

from urban_json.errors import JsltError

from ._helpers import to_text
from .registry import jslt_function

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


@jslt_function("regexismatch", description="Vrai si le texte contient une correspondance du motif regex", description_en="True when the text holds a match of the regex pattern")
def execute_regexismatch(ctx: Any, token: Any = None, pattern: str = "") -> Any:
    subject = _regex_subject(token)
    if subject is None:
        return None
    # search, pas match : Regex.IsMatch .NET n'est pas ancré au début.
    return _compile(pattern).search(subject) is not None


@jslt_function("regexmatches", description="Liste des correspondances du motif regex dans le texte", description_en="List of the matches of the regex pattern in the text")
def execute_regexmatches(ctx: Any, token: Any = None, pattern: str = "") -> Any:
    subject = _regex_subject(token)
    if subject is None:
        return None
    # group(0) = correspondance complète (Match.Value .NET) ; findall renverrait
    # les groupes capturés dès qu'il y en a.
    return [m.group(0) for m in _compile(pattern).finditer(subject)]


# Syntaxe de substitution .NET -> celle du module `re` : sans cette traduction,
# un `$1` écrit pour le .NET serait recopié littéralement dans le résultat.
_DOTNET_SUBSTITUTION = re.compile(r"\$(\$|&|[0-9]+|\{\w+\})")


def _substitution(replacement: str) -> str:
    def convert(match: re.Match[str]) -> str:
        token = match.group(1)
        if token == "$":
            return "$"
        if token == "&":
            return r"\g<0>"
        name = token[1:-1] if token.startswith("{") else token
        return f"\\g<{name}>"

    # Les antislashs du remplacement sont littéraux en .NET : on les protège
    # avant d'introduire les nôtres, sinon `\t` écrit par l'auteur deviendrait
    # une tabulation.
    return _DOTNET_SUBSTITUTION.sub(convert, replacement.replace("\\", "\\\\"))


@jslt_function(
    "regexreplace",
    description="Remplace les correspondances d'un motif regex ($1, ${nom}, $& pour les groupes)",
    description_en="Replaces the matches of a regex pattern ($1, ${name}, $& for the groups)",
)
def execute_regexreplace(
    ctx: Any, token: Any = None, pattern: Any = None, replacement: Any = None
) -> Any:
    subject = _regex_subject(token)
    if subject is None:
        return None
    return _compile(pattern).sub(_substitution(to_text(replacement)), subject)


@jslt_function(
    "splitregex",
    description="Découpe un texte sur les correspondances d'un motif regex",
    description_en="Cuts a text on the matches of a regex pattern",
)
def execute_splitregex(ctx: Any, token: Any = None, pattern: Any = None, limit: Any = None) -> Any:
    """Découpe sur un motif, pour les séparateurs à géométrie variable
    (« a ; b;c »), que ni `split` ni `splitstring` ne savent couper."""
    subject = _regex_subject(token)
    if subject is None:
        return None
    cuts = 0 if limit is None else int(limit)
    return _compile(pattern).split(subject, maxsplit=cuts)
