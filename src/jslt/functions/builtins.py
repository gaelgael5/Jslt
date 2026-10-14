"""Fonctions intégrées du cœur jslt.

Portage d'un sous-ensemble des ``CustomServices`` .NET. Chaque fonction reçoit le
contexte d'exécution en premier argument, puis les arguments JSON évalués.

Couverture actuelle (Phase 4a) : ``sum``, ``concat``. D'autres fonctions pures
(distinct, count…) viendront ensuite ; les fonctions d'E-S restent hors cœur.
"""

from __future__ import annotations

from typing import Any

from jslt.errors import JsltError

from .registry import jslt_function


@jslt_function("sum")
def execute_sum(ctx: Any, token: Any = None) -> Any:
    """Somme des éléments numériques d'un tableau (port de ``ExecuteSum``).

    Un tableau vide ou ``None`` donne 0. La somme reste entière si tous les
    éléments sont entiers.
    """
    if token is None:
        return 0
    if isinstance(token, list):
        total: Any = 0
        for item in token:
            if isinstance(item, bool) or not isinstance(item, (int, float)):
                raise JsltError("sum attend des entiers ou des flottants")
            total += item
        return total
    if isinstance(token, (int, float)) and not isinstance(token, bool):
        return token
    raise JsltError("sum attend un tableau")


@jslt_function("concat")
def execute_concat(
    ctx: Any, token: Any = None, split_char: str | None = None, delimit_char: str | None = None
) -> str:
    """Concatène les éléments d'un tableau en chaîne (port de ``ExecuteConcat``).

    ``split_char`` et ``delimit_char`` composent le séparateur inséré entre les
    éléments (leur concaténation), vide par défaut.
    """
    separator = (split_char or "") + (delimit_char or "")
    if token is None:
        return ""
    if isinstance(token, list):
        return separator.join(_to_text(item) for item in token)
    return _to_text(token)


def _to_text(value: Any) -> str:
    if value is None:
        return ""
    if value is True:
        return "True"
    if value is False:
        return "False"
    return str(value)
