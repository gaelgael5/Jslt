"""Fonctions diverses : uuid, now, isnull, isnotnull (port des ``Services`` .NET).

``uuid`` et ``now`` sont non déterministes (générées à l'exécution). Les autres
fonctions de dates — ``parsedate``, ``dateadd``, ``datesub``, ``datepart`` —
vivent dans :mod:`.dates`.
"""

from __future__ import annotations

import uuid as _uuid
from datetime import datetime, timezone
from typing import Any

from .registry import jslt_function


@jslt_function("uuid", description="Nouvel identifiant unique aléatoire (UUID v4) à chaque appel")
def execute_uuid(ctx: Any) -> str:
    return str(_uuid.uuid4())


@jslt_function("now", description="Date et heure courantes en ISO 8601 : locales, ou UTC si utc vaut true")
def execute_now(ctx: Any, utc: bool = False) -> str:
    # L'heure locale (sans tz) est volontaire : `now(false)` renvoie l'heure
    # locale, `now(true)` l'UTC — fidèle au comportement .NET.
    moment = datetime.now(timezone.utc) if utc else datetime.now()  # noqa: DTZ005
    return moment.isoformat()


@jslt_function("isnull", description="Vrai si la valeur est null ou absente")
def execute_isnull(ctx: Any, token: Any = None) -> bool:
    return token is None


@jslt_function("isnotnull", description="Vrai si la valeur n'est ni null ni absente")
def execute_isnotnull(ctx: Any, token: Any = None) -> bool:
    return token is not None
