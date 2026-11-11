"""Fonctions diverses : ``uuid``, ``now``, ``isnull``, ``isnotnull`` (port des
``Services`` .NET), et les paramètres externes ``param`` / ``params``.

``uuid`` et ``now`` sont non déterministes (générées à l'exécution). Les
fonctions de dates — ``parsedate``, ``dateadd``, ``datesub``, ``datediff``,
``datepart``… — vivent dans :mod:`.dates`.
"""

from __future__ import annotations

import uuid as _uuid
from datetime import datetime, timezone
from typing import Any

from urban_json.errors import JsltError

from ._helpers import to_text
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


@jslt_function(
    "param",
    description="Valeur d'un paramètre externe passé à transform, ou la valeur de repli",
)
def execute_param(ctx: Any, name: Any = None, default: Any = None) -> Any:
    """Réglage externe de l'exécution (``transform(source, parameters={...})``).

    Un paramètre **fourni à ``null``** reste ``null`` : le repli ne s'applique
    qu'à un paramètre absent. Confondre les deux empêcherait de passer
    explicitement « pas de valeur ».
    """
    if name is None or to_text(name).strip() == "":
        raise JsltError("param attend le nom du paramètre")
    key = to_text(name).strip()
    # `.get` et non `?? default` : il rend la valeur stockée même nulle, donc un
    # paramètre passé explicitement à null n'est pas écrasé par le repli.
    return getattr(ctx, "parameters", {}).get(key, default)


@jslt_function(
    "params",
    description="Tous les paramètres externes de l'exécution, sous forme d'objet",
)
def execute_params(ctx: Any) -> dict:
    """Vue d'ensemble des paramètres — utile pour les recopier dans une sortie
    (traçabilité d'un lot) sans les énumérer un par un."""
    return dict(getattr(ctx, "parameters", {}))
