"""Fonctions diverses : uuid, now, isnull, isnotnull (port des ``Services`` .NET).

``uuid`` et ``now`` sont non déterministes (générées à l'exécution).
"""

from __future__ import annotations

import re
import uuid as _uuid
from datetime import datetime, timezone
from typing import Any

from urban_json.errors import JsltError

from .registry import jslt_function


@jslt_function("uuid")
def execute_uuid(ctx: Any) -> str:
    return str(_uuid.uuid4())


@jslt_function("now")
def execute_now(ctx: Any, utc: bool = False) -> str:
    # L'heure locale (sans tz) est volontaire : `now(false)` renvoie l'heure
    # locale, `now(true)` l'UTC — fidèle au comportement .NET.
    moment = datetime.now(timezone.utc) if utc else datetime.now()  # noqa: DTZ005
    return moment.isoformat()


@jslt_function("isnull")
def execute_isnull(ctx: Any, token: Any = None) -> bool:
    return token is None


@jslt_function("isnotnull")
def execute_isnotnull(ctx: Any, token: Any = None) -> bool:
    return token is not None


# Cultures qui lisent « 10/22/2026 » mois d'abord (comme la culture invariante
# .NET) ; toutes les autres lisent jour d'abord (fr-FR, de-DE, en-GB…).
_MONTH_FIRST = {"", "invariant", "en", "en-us"}
_NUMERIC_DATE = re.compile(
    r"^(\d{1,4})[./-](\d{1,2})[./-](\d{1,4})"
    r"(?:[ T](\d{1,2}):(\d{2})(?::(\d{2}))?)?$"
)


def _full_year(year: int, digits: int) -> int:
    # Année sur deux chiffres : fenêtre .NET par défaut (TwoDigitYearMax = 2049).
    if digits > 2:
        return year
    return 2000 + year if year <= 49 else 1900 + year


@jslt_function("parsedate", description="Lit une date texte selon une culture (ex. fr-FR), rendue en ISO 8601")
def execute_parsedate(ctx: Any, token: Any = None, culture: Any = None) -> Any:
    """Port de ``ExecuteParseDate`` (``DateTime.Parse`` avec culture). Le portage
    n'a pas de type date : le résultat est la chaîne ISO 8601. Reconnus : ISO
    8601, et les dates numériques ``j/m/a`` ou ``m/j/a`` (séparateurs ``/ . -``)
    avec une heure optionnelle ``HH:mm[:ss]`` ; ``aaaa/m/j`` si l'année est en
    tête. Une valeur non textuelle est rendue telle quelle, comme en .NET."""
    if not isinstance(token, str):
        return token
    text = token.strip()
    try:
        return datetime.fromisoformat(text).isoformat()
    except ValueError:
        pass
    match = _NUMERIC_DATE.match(text)
    if match is None:
        raise JsltError(f"date illisible : {token!r}")
    first, second, third, hour, minute, sec = match.groups()
    if len(first) == 4:
        year, month, day = int(first), int(second), int(third)
    else:
        year = _full_year(int(third), len(third))
        month_first = str(culture or "").strip().lower() in _MONTH_FIRST
        month, day = (int(first), int(second)) if month_first else (int(second), int(first))
    try:
        # Sans fuseau, volontairement : DateTime.Parse .NET rend une date « Unspecified ».
        moment = datetime(year, month, day, int(hour or 0), int(minute or 0), int(sec or 0))  # noqa: DTZ001
    except ValueError as exc:
        raise JsltError(f"date invalide : {token!r} ({exc})") from exc
    return moment.isoformat()
