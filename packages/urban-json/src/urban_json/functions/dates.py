"""Fonctions de dates : ``parsedate``, ``dateadd``, ``datesub``, ``datediff``,
``datepart``.

Le .NET n'offrait que ``parsedate(texte, culture)`` ; le calcul et l'extraction
n'existaient nulle part, et les templates contournaient par du découpage de
chaîne. Tout passe par la même représentation que le reste du portage : il n'y a
pas de type date, une date est une **chaîne ISO 8601** (celle que rendent
``now``, ``parsedate`` et ces fonctions, celle que lit ``format``).

``null`` est propagé tel quel (données creuses), mais une valeur qui n'est pas
une date ISO lève : la rendre ``null`` ferait découvrir le problème de données
très loin de sa cause.
"""

from __future__ import annotations

import calendar
from datetime import datetime, timedelta
from typing import Any

from urban_json.errors import JsltError

from ._dateread import as_moment, detect_date, in_zone, parse_with_mask
from ._helpers import is_number, to_text
from .registry import jslt_function

# Unités de `dateadd`/`datesub` à durée fixe → nom du paramètre de `timedelta`.
# `month` et `year` en sont absents volontairement : leur durée dépend du mois
# visé, ils passent par `_add_months` (bornage du jour).
_FIXED_UNITS = {
    "second": "seconds",
    "minute": "minutes",
    "hour": "hours",
    "day": "days",
    "week": "weeks",
}
_UNITS = (*_FIXED_UNITS, "month", "year")

# Durée d'une unité fixe, dérivée de `_FIXED_UNITS` plutôt que recopiée : deux
# tables aux mêmes clefs finissent par divergir.
_UNIT_SECONDS = {
    unit: int(timedelta(**{parameter: 1}).total_seconds())
    for unit, parameter in _FIXED_UNITS.items()
}

_PARTS = ("year", "month", "day", "dayofweek", "hour", "minute", "second")


@jslt_function(
    "parsedate",
    description=(
        "Lit une date texte et la rend en ISO 8601 : détection selon la culture, "
        "ou masque explicite (dd/MM/yyyy…), avec un fuseau optionnel"
    ),
)
def execute_parsedate(
    ctx: Any, token: Any = None, culture: Any = None, mask: Any = None, timezone: Any = None
) -> Any:
    """Lit une date texte (``ExecuteParseDate`` du .NET, étendu).

    Sans ``mask``, la date est détectée : ISO 8601, ou numérique ``j/m/a`` /
    ``m/j/a`` selon ``culture`` (séparateurs ``/ . -``), heure ``HH:mm[:ss]``
    optionnelle, ``aaaa/m/j`` si l'année est en tête. Avec ``mask``, la lecture
    suit le masque .NET (cf. :mod:`._datemask`). ``timezone`` accepte un nom
    IANA (``Europe/Paris``), ``UTC``/``Z`` ou un décalage fixe (``+02:00``) :
    il **qualifie** une date sans décalage, et **convertit** une date qui en
    porte un. Une valeur non textuelle est rendue telle quelle, comme en .NET.
    """
    if not isinstance(token, str):
        return token
    text = token.strip()
    mask_text = "" if mask is None else to_text(mask).strip()
    moment = parse_with_mask(text, mask_text, culture) if mask_text else detect_date(text, culture)
    zone_text = "" if timezone is None else to_text(timezone).strip()
    if zone_text:
        moment = in_zone(moment, zone_text)
    return moment.isoformat()


@jslt_function(
    "dateadd",
    description=(
        "Ajoute une durée à une date ISO 8601 : unité second, minute, hour, day, "
        "week, month ou year, et un nombre entier (négatif pour retrancher)"
    ),
)
def execute_dateadd(ctx: Any, token: Any = None, unit: Any = None, amount: Any = None) -> Any:
    """Décale une date d'un nombre entier d'unités.

    ``month`` et ``year`` sont calendaires : le jour est **borné** au dernier
    jour du mois visé (31 janvier + 1 mois = 28 février), comme ``AddMonths``
    en .NET. Le décalage horaire de l'entrée est conservé tel quel.
    """
    if token is None:
        return None
    return _add(as_moment(token), _unit(unit), _whole(amount)).isoformat()


@jslt_function(
    "datesub",
    description=(
        "Retranche une durée à une date ISO 8601 : unité second, minute, hour, day, "
        "week, month ou year, et un nombre entier"
    ),
)
def execute_datesub(ctx: Any, token: Any = None, unit: Any = None, amount: Any = None) -> Any:
    """Inverse de ``dateadd`` : ``datesub(d, u, n)`` vaut ``dateadd(d, u, -n)``."""
    if token is None:
        return None
    return _add(as_moment(token), _unit(unit), -_whole(amount)).isoformat()


@jslt_function(
    "datepart",
    description=(
        "Extrait une composante entière d'une date ISO 8601 : year, month, day, "
        "dayofweek (dimanche = 0), hour, minute ou second"
    ),
)
def execute_datepart(ctx: Any, token: Any = None, part: Any = None) -> Any:
    """Rend une composante de la date, en nombre.

    ``dayofweek`` suit la convention ``DayOfWeek`` du .NET — dimanche = 0,
    samedi = 6 — et non ISO (lundi = 1), pour qu'un template écrit pour le .NET
    donne le même résultat.
    """
    if token is None:
        return None
    moment = as_moment(token)
    name = to_text(part).strip().lower()
    if name == "dayofweek":
        return (moment.weekday() + 1) % 7
    if name in _PARTS:
        return getattr(moment, name)
    raise JsltError(f"partie de date inconnue : {to_text(part)!r} (attendu : {', '.join(_PARTS)})")


@jslt_function(
    "datediff",
    description=(
        "Compte les unités entières écoulées entre deux dates ISO 8601 : second, "
        "minute, hour, day, week, month ou year, négatif si la fin précède le début"
    ),
)
def execute_datediff(ctx: Any, start: Any = None, end: Any = None, unit: Any = None) -> Any:
    """Écart entre deux dates, en unités **entières**.

    Le compte est tronqué **vers zéro** : 36 heures font 1 jour, 12 heures en
    font 0, et -36 heures en font -1. `month` et `year` sont calendaires — un
    mois n'est entier que si le jour et l'heure de `end` ont atteint ceux de
    `start`. Corollaire : `datediff` n'inverse pas exactement `dateadd` sur ces
    deux unités, parce que `dateadd` borne le jour sur les mois courts (du
    31 janvier, `dateadd` d'un mois donne le 28 février, dont `datediff` compte
    0 mois entier).
    """
    if start is None or end is None:
        return None
    return _diff(as_moment(start), as_moment(end), _unit(unit))


# --- calcul -------------------------------------------------------------------


def _unit(unit: Any) -> str:
    name = to_text(unit).strip().lower()
    # Pluriel toléré ('days' comme 'day') : les deux formes s'écrivent
    # spontanément et refuser l'une n'apporte rien.
    singular = name[:-1] if name.endswith("s") and name[:-1] in _UNITS else name
    if singular not in _UNITS:
        raise JsltError(f"unité de date inconnue : {to_text(unit)!r} (attendu : {', '.join(_UNITS)})")
    return singular


def _whole(amount: Any) -> int:
    if not is_number(amount) or int(amount) != amount:
        raise JsltError(f"nombre entier d'unités attendu, reçu : {amount!r}")
    return int(amount)


def _add(moment: datetime, unit: str, amount: int) -> datetime:
    if unit == "month":
        return _add_months(moment, amount)
    if unit == "year":
        return _add_months(moment, 12 * amount)
    return moment + timedelta(**{_FIXED_UNITS[unit]: amount})


def _add_months(moment: datetime, months: int) -> datetime:
    total = moment.month - 1 + months
    year = moment.year + total // 12
    month = total % 12 + 1
    # Bornage : le 31 d'un mois de 30 jours n'existe pas, .NET garde le dernier
    # jour du mois visé plutôt que de déborder sur le suivant.
    day = min(moment.day, calendar.monthrange(year, month)[1])
    try:
        return moment.replace(year=year, month=month, day=day)
    except ValueError as exc:
        raise JsltError(f"date hors bornes après décalage de {months} mois ({exc})") from exc


def _diff(start: datetime, end: datetime, unit: str) -> int:
    # Soustraire une date naïve d'une date avec fuseau n'a pas de sens (Python
    # lèverait un TypeError brut) : on le dit, plutôt que de supposer un fuseau.
    if (start.tzinfo is None) != (end.tzinfo is None):
        raise JsltError(
            "écart impossible : une date porte un fuseau horaire et l'autre non "
            f"({start.isoformat()!r}, {end.isoformat()!r})"
        )
    if unit in ("month", "year"):
        months = _whole_months(start, end)
        return months if unit == "month" else int(months / 12)
    return _toward_zero(int((end - start).total_seconds()), _UNIT_SECONDS[unit])


def _toward_zero(total: int, size: int) -> int:
    # `//` arrondirait vers moins l'infini : -36 h donneraient -2 jours.
    sign = -1 if total < 0 else 1
    return sign * (abs(total) // size)


def _whole_months(start: datetime, end: datetime) -> int:
    if end.tzinfo is not None:
        # Même décalage avant de comparer des composantes de calendrier, sinon
        # 23:45-01:00 passerait pour antérieur à 00:30+01:00 alors qu'il suit.
        end = end.astimezone(start.tzinfo)
    months = (end.year - start.year) * 12 + end.month - start.month
    end_position, start_position = _within_month(end), _within_month(start)
    if months > 0 and end_position < start_position:
        return months - 1
    if months < 0 and end_position > start_position:
        return months + 1
    return months


def _within_month(moment: datetime) -> tuple[int, ...]:
    """Position dans le mois, pour savoir si le mois entamé est révolu."""
    return (moment.day, moment.hour, moment.minute, moment.second, moment.microsecond)
