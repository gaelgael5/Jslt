"""Helpers partagés par les fonctions intégrées (coercions et conventions .NET)."""

from __future__ import annotations

import json
from typing import Any


def to_text(value: Any) -> str:
    """Représentation chaîne façon .NET (``True``/``False`` capitalisés)."""
    if value is None:
        return ""
    if value is True:
        return "True"
    if value is False:
        return "False"
    return str(value)


def stringify(value: Any) -> str:
    """Équivalent de ``token.ToString()`` : scalaires en texte, objets/tableaux en JSON."""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return to_text(value)


def is_number(value: Any) -> bool:
    """Vrai pour int/float, mais pas pour les booléens (comme en JSON/jslt)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def coerce_number(value: Any) -> int | float:
    if value is None:
        return 0
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return float(value)
    raise ValueError(f"conversion numérique impossible : {value!r}")


def coerce_bool(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        low = value.strip().lower()
        if low in ("true", "false"):
            return low == "true"
    return bool(value)


def string_result(token: Any, fn):
    """Convention .NET des fonctions de chaîne : None->None, str->fn(str), autre->False."""
    if token is None:
        return None
    if isinstance(token, str):
        return fn(token)
    return False


def number_result(token: Any, fn):
    """Convention .NET des fonctions numériques : non-nombre (ou None) -> None."""
    if not is_number(token):
        return None
    return fn(token)
