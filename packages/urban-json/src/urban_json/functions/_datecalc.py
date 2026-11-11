"""Calcul sur les dates : unités, décalage, écart, bornes de période, durée.

Séparé de :mod:`.dates` (qui enregistre les fonctions) pour la même raison que
:mod:`._dateread` l'est : lire du texte, calculer, et exposer au langage sont
trois métiers, et un seul fichier les mêlant dépasse vite ce qu'on relit d'un
trait.

Deux conventions traversent ce module :

* les unités de calendrier (``month``, ``year``) **bornent** le jour sur les mois
  courts, comme ``AddMonths`` en .NET ;
* ``weekday`` compte les jours ouvrés du lundi au vendredi. Aucun calendrier de
  jours fériés n'est appliqué : il dépend du pays, de l'année et parfois de
  l'entreprise, et en embarquer un ici donnerait des résultats faux et
  silencieux hors de son périmètre.
"""

from __future__ import annotations

import calendar
from datetime import datetime, timedelta
from typing import Any

from urban_json.errors import JsltError

from ._helpers import is_number, to_text

# Unités de `dateadd`/`datesub` à durée fixe → nom du paramètre de `timedelta`.
# `month` et `year` en sont absents volontairement : leur durée dépend du mois
# visé, ils passent par `_add_months` (bornage du jour).
FIXED_UNITS = {
    "second": "seconds",
    "minute": "minutes",
    "hour": "hours",
    "day": "days",
    "week": "weeks",
}
UNITS = (*FIXED_UNITS, "weekday", "month", "year")

# Durée d'une unité fixe, dérivée de `FIXED_UNITS` plutôt que recopiée : deux
# tables aux mêmes clefs finissent par divergir.
UNIT_SECONDS = {
    unit: int(timedelta(**{parameter: 1}).total_seconds())
    for unit, parameter in FIXED_UNITS.items()
}

PARTS = (
    "year", "quarter", "month", "week", "day", "dayofyear", "dayofweek",
    "hour", "minute", "second", "millisecond",
)



# Unités de bornage de période (`datestartof` / `dateendof`), de la plus large à
# la plus fine : `second` en est absent, borner à la seconde n'a pas d'usage.
_PERIODS = ("year", "quarter", "month", "week", "day", "hour", "minute")

# --- décalage et écart -------------------------------------------------------------------


def unit_of(unit: Any) -> str:
    name = to_text(unit).strip().lower()
    # Pluriel toléré ('days' comme 'day') : les deux formes s'écrivent
    # spontanément et refuser l'une n'apporte rien.
    singular = name[:-1] if name.endswith("s") and name[:-1] in UNITS else name
    if singular not in UNITS:
        raise JsltError(f"unité de date inconnue : {to_text(unit)!r} (attendu : {', '.join(UNITS)})")
    return singular


def whole_amount(amount: Any) -> int:
    if not is_number(amount) or int(amount) != amount:
        raise JsltError(f"nombre entier d'unités attendu, reçu : {amount!r}")
    return int(amount)


def add_units(moment: datetime, unit: str, amount: int) -> datetime:
    if unit == "weekday":
        return add_weekdays(moment, amount)
    if unit == "month":
        return add_months(moment, amount)
    if unit == "year":
        return add_months(moment, 12 * amount)
    return moment + timedelta(**{FIXED_UNITS[unit]: amount})


def add_weekdays(moment: datetime, amount: int) -> datetime:
    """Décale de ``amount`` jours ouvrés (lundi-vendredi), week-ends sautés.

    Pas de formule : on avance jour par jour. Un décalage de jours ouvrés se
    compte en dizaines, jamais en millions, et une formule modulo 5 est l'endroit
    exact où se glissent les erreurs de bord (départ un samedi, amount nul).
    """
    step = 1 if amount >= 0 else -1
    remaining = abs(amount)
    result = moment
    while remaining:
        result += timedelta(days=step)
        if result.weekday() < 5:
            remaining -= 1
    return result


def weekdays_between(start: datetime, whole_days: int) -> int:
    """Jours ouvrés parmi ``whole_days`` jours pleins écoulés depuis ``start``."""
    step = 1 if whole_days >= 0 else -1
    weeks, rest = divmod(abs(whole_days), 7)
    count = weeks * 5  # toute semaine pleine porte exactement 5 jours ouvrés
    day = start + timedelta(days=step * weeks * 7)
    for _ in range(rest):
        day += timedelta(days=step)
        if day.weekday() < 5:
            count += 1
    return step * count


def add_months(moment: datetime, months: int) -> datetime:
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


def guard_same_kind(start: datetime, end: datetime) -> None:
    """Refuse de comparer une date avec fuseau à une date sans fuseau.

    Python lèverait un ``TypeError`` brut ; supposer un fuseau inventerait une
    donnée, et l'écart serait faux de quelques heures sans que rien ne le dise.
    """
    if (start.tzinfo is None) != (end.tzinfo is None):
        raise JsltError(
            "écart impossible : une date porte un fuseau horaire et l'autre non "
            f"({start.isoformat()!r}, {end.isoformat()!r})"
        )


def diff_units(start: datetime, end: datetime, unit: str) -> int:
    guard_same_kind(start, end)
    if unit == "weekday":
        whole_days = toward_zero(int((end - start).total_seconds()), UNIT_SECONDS["day"])
        return weekdays_between(start, whole_days)
    if unit in ("month", "year"):
        months = whole_months(start, end)
        return months if unit == "month" else int(months / 12)
    return toward_zero(int((end - start).total_seconds()), UNIT_SECONDS[unit])


def toward_zero(total: int, size: int) -> int:
    # `//` arrondirait vers moins l'infini : -36 h donneraient -2 jours.
    sign = -1 if total < 0 else 1
    return sign * (abs(total) // size)


def whole_months(start: datetime, end: datetime) -> int:
    if end.tzinfo is not None:
        # Même décalage avant de comparer des composantes de calendrier, sinon
        # 23:45-01:00 passerait pour antérieur à 00:30+01:00 alors qu'il suit.
        end = end.astimezone(start.tzinfo)
    months = (end.year - start.year) * 12 + end.month - start.month
    end_position, start_position = within_month(end), within_month(start)
    if months > 0 and end_position < start_position:
        return months - 1
    if months < 0 and end_position > start_position:
        return months + 1
    return months


def within_month(moment: datetime) -> tuple[int, ...]:
    """Position dans le mois, pour savoir si le mois entamé est révolu."""
    return (moment.day, moment.hour, moment.minute, moment.second, moment.microsecond)


# --- parties, bornes de période et durée -------------------------------------


def part_of(moment: datetime, name: str) -> int:
    """Composante entière d'une date (``datepart``)."""
    if name == "dayofweek":
        # Convention `DayOfWeek` du .NET : dimanche = 0, pas ISO (lundi = 1).
        return (moment.weekday() + 1) % 7
    if name == "dayofyear":
        return moment.timetuple().tm_yday
    if name == "week":
        # Semaine ISO : le 1er janvier appartient parfois à la semaine 52/53 de
        # l'année précédente, et c'est la définition attendue en Europe.
        return moment.isocalendar()[1]
    if name == "quarter":
        return (moment.month - 1) // 3 + 1
    if name == "millisecond":
        return moment.microsecond // 1000
    return getattr(moment, name)


def period_of(period: Any) -> str:
    name = to_text(period).strip().lower()
    if name not in _PERIODS:
        raise JsltError(
            f"unité de période inconnue : {to_text(period)!r} (attendu : {', '.join(_PERIODS)})"
        )
    return name


def start_of(moment: datetime, period: str) -> datetime:
    """Premier instant de la période contenant ``moment`` (fuseau conservé)."""
    if period == "minute":
        return moment.replace(second=0, microsecond=0)
    floored = moment.replace(minute=0, second=0, microsecond=0)
    if period == "hour":
        return floored
    midnight = floored.replace(hour=0)
    if period == "day":
        return midnight
    if period == "week":
        # Semaine ISO, du lundi : `dayofweek` suit le .NET (dimanche = 0) mais
        # borner une semaine au dimanche surprendrait tout lecteur européen.
        return midnight - timedelta(days=midnight.weekday())
    if period == "month":
        return midnight.replace(day=1)
    if period == "quarter":
        return midnight.replace(month=(moment.month - 1) // 3 * 3 + 1, day=1)
    return midnight.replace(month=1, day=1)


def end_of(moment: datetime, period: str) -> datetime:
    """Dernier instant de la période : début de la suivante, moins 1 µs.

    La microseconde est la plus petite unité que porte une date ISO ici ; une
    borne de fin « inclusive » est ce qu'attend un filtre ``<=``.
    """
    return _next_period(start_of(moment, period), period) - timedelta(microseconds=1)


def _next_period(start: datetime, period: str) -> datetime:
    if period == "minute":
        return start + timedelta(minutes=1)
    if period == "hour":
        return start + timedelta(hours=1)
    if period == "day":
        return start + timedelta(days=1)
    if period == "week":
        return start + timedelta(days=7)
    if period == "month":
        return add_months(start, 1)
    if period == "quarter":
        return add_months(start, 3)
    return add_months(start, 12)


def duration_between(start: datetime, end: datetime) -> dict[str, Any]:
    """Décomposition calendaire d'un intervalle (années, mois, jours, h, min, s).

    Un objet plutôt qu'un texte « il y a 3 jours » : la mise en forme dépend de
    la langue et du contexte, et le template sait la faire ; le moteur, lui,
    n'embarque pas de catalogue de phrases.
    """
    guard_same_kind(start, end)
    negative = end < start
    first, second = (end, start) if negative else (start, end)
    months = whole_months(first, second)
    anchor = add_months(first, months)
    rest = second - anchor
    hours, remainder = divmod(rest.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return {
        "negative": negative,
        "years": months // 12,
        "months": months % 12,
        "days": rest.days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
    }
