"""Fonctions de chaîne intégrées (port des ``Services.strings`` .NET).

Convention : ``None`` -> ``None``, chaîne -> résultat, autre valeur -> ``False``
(sauf ``stringlenght`` qui suit sa propre convention .NET).
"""

from __future__ import annotations

from typing import Any

from ._helpers import string_result
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
