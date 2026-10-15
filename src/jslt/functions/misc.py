"""Fonctions diverses : uuid, now, isnull, isnotnull (port des ``Services`` .NET).

``uuid`` et ``now`` sont non déterministes (générées à l'exécution).
"""

from __future__ import annotations

import uuid as _uuid
from datetime import datetime, timezone
from typing import Any

from .registry import jslt_function


@jslt_function("uuid")
def execute_uuid(ctx: Any) -> str:
    return str(_uuid.uuid4())


@jslt_function("now")
def execute_now(ctx: Any, utc: bool = False) -> str:
    moment = datetime.now(timezone.utc) if utc else datetime.now()
    return moment.isoformat()


@jslt_function("isnull")
def execute_isnull(ctx: Any, token: Any = None) -> bool:
    return token is None


@jslt_function("isnotnull")
def execute_isnotnull(ctx: Any, token: Any = None) -> bool:
    return token is not None
