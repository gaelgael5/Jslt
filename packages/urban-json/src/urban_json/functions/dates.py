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

from datetime import datetime, timezone
from typing import Any

from urban_json.errors import JsltError

from ._datecalc import (
    PARTS,
    add_units,
    diff_units,
    duration_between,
    end_of,
    part_of,
    period_of,
    start_of,
    unit_of,
    whole_amount,
)
from ._dateread import as_moment, detect_date, in_zone, parse_with_mask, resolve_zone
from ._helpers import coerce_bool, to_text
from .registry import jslt_function


@jslt_function(
    "parsedate",
    description=(
        "Lit une date texte et la rend en ISO 8601 : détection selon la culture, "
        "ou masque explicite (dd/MM/yyyy…), avec un fuseau optionnel"
    ),
    description_en="Reads a date from text and returns it in ISO 8601: detection by culture, or an explicit mask (dd/MM/yyyy…), with an optional timezone",
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
    description_en="Adds a duration to an ISO 8601 date: unit second, minute, hour, day, week, month or year, and a whole number (negative to subtract)",
)
def execute_dateadd(ctx: Any, token: Any = None, unit: Any = None, amount: Any = None) -> Any:
    """Décale une date d'un nombre entier d'unités.

    ``month`` et ``year`` sont calendaires : le jour est **borné** au dernier
    jour du mois visé (31 janvier + 1 mois = 28 février), comme ``AddMonths``
    en .NET. Le décalage horaire de l'entrée est conservé tel quel.
    """
    if token is None:
        return None
    return add_units(as_moment(token), unit_of(unit), whole_amount(amount)).isoformat()


@jslt_function(
    "datesub",
    description=(
        "Retranche une durée à une date ISO 8601 : unité second, minute, hour, day, "
        "week, month ou year, et un nombre entier"
    ),
    description_en="Subtracts a duration from an ISO 8601 date: unit second, minute, hour, day, week, month or year, and a whole number",
)
def execute_datesub(ctx: Any, token: Any = None, unit: Any = None, amount: Any = None) -> Any:
    """Inverse de ``dateadd`` : ``datesub(d, u, n)`` vaut ``dateadd(d, u, -n)``."""
    if token is None:
        return None
    return add_units(as_moment(token), unit_of(unit), -whole_amount(amount)).isoformat()


@jslt_function(
    "datepart",
    description=(
        "Extrait une composante entière d'une date ISO 8601 : year, month, day, "
        "dayofweek (dimanche = 0), hour, minute ou second"
    ),
    description_en="Extracts a whole component from an ISO 8601 date: year, month, day, dayofweek (Sunday = 0), hour, minute or second",
)
def execute_datepart(ctx: Any, token: Any = None, part: Any = None) -> Any:
    """Rend une composante de la date, en nombre.

    ``dayofweek`` suit la convention ``DayOfWeek`` du .NET — dimanche = 0,
    samedi = 6 — et non ISO (lundi = 1), pour qu'un template écrit pour le .NET
    donne le même résultat.
    """
    if token is None:
        return None
    name = to_text(part).strip().lower()
    if name not in PARTS:
        raise JsltError(
            f"partie de date inconnue : {to_text(part)!r} (attendu : {', '.join(PARTS)})"
        )
    return part_of(as_moment(token), name)


@jslt_function(
    "datediff",
    description=(
        "Compte les unités entières écoulées entre deux dates ISO 8601 : second, "
        "minute, hour, day, week, month ou year, négatif si la fin précède le début"
    ),
    description_en="Counts the whole units elapsed between two ISO 8601 dates: second, minute, hour, day, week, month or year, negative when the end precedes the start",
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
    return diff_units(as_moment(start), as_moment(end), unit_of(unit))




@jslt_function(
    "datestartof",
    description=(
        "Premier instant de la période contenant la date : year, quarter, month, "
        "week (lundi), day, hour ou minute"
    ),
    description_en="First instant of the period holding the date: year, quarter, month, week (Monday), day, hour or minute",
)
def execute_datestartof(ctx: Any, token: Any = None, period: Any = None) -> Any:
    """Borne basse d'une période, décalage horaire conservé."""
    if token is None:
        return None
    return start_of(as_moment(token), period_of(period)).isoformat()


@jslt_function(
    "dateendof",
    description=(
        "Dernier instant de la période contenant la date (borne inclusive, à la "
        "microseconde près)"
    ),
    description_en="Last instant of the period holding the date (inclusive bound, to the microsecond)",
)
def execute_dateendof(ctx: Any, token: Any = None, period: Any = None) -> Any:
    if token is None:
        return None
    return end_of(as_moment(token), period_of(period)).isoformat()


@jslt_function(
    "datezone",
    description=(
        "Attribue un fuseau à une date sans décalage, ou convertit une date qui "
        "en porte déjà un"
    ),
    description_en="Attaches a timezone to a date without offset, or converts a date that already carries one",
)
def execute_datezone(ctx: Any, token: Any = None, zone: Any = None) -> Any:
    """Conversion de fuseau explicite.

    C'était faisable par le détour ``parsedate(date, "", "", "Europe/Paris")`` :
    une date déjà lue n'a pas à repasser par une fonction de lecture pour changer
    de fuseau.
    """
    if token is None:
        return None
    text = to_text(zone).strip()
    if not text:
        raise JsltError("datezone attend un fuseau horaire (nom IANA, UTC ou décalage fixe)")
    resolve_zone(text)  # échoue tôt, avec le nom du fuseau fautif
    return in_zone(as_moment(token), text).isoformat()


@jslt_function(
    "today",
    description="Date du jour à minuit en ISO 8601 : locale, ou UTC si utc vaut true",
    description_en="Today's date at midnight in ISO 8601: local, or UTC when utc is true",
)
def execute_today(ctx: Any, utc: Any = False) -> str:
    """Minuit du jour courant — ``now`` porte l'heure, ce qui empêche de comparer
    deux journées sans tronquer à la main."""
    moment = datetime.now(timezone.utc) if coerce_bool(utc) else datetime.now()  # noqa: DTZ005
    return moment.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()


@jslt_function(
    "dateduration",
    description=(
        "Décompose l'intervalle entre deux dates en années, mois, jours, heures, "
        "minutes et secondes"
    ),
    description_en="Splits the interval between two dates into years, months, days, hours, minutes and seconds",
)
def execute_dateduration(ctx: Any, start: Any = None, end: Any = None) -> Any:
    """Durée décomposée, avec un drapeau ``negative`` si la fin précède le début.

    ``datediff`` répond « combien d'unités » dans **une** unité ; ici on veut la
    lecture humaine complète (1 an, 1 mois, 2 jours…), que le template met en
    forme dans sa langue.
    """
    if start is None or end is None:
        return None
    return duration_between(as_moment(start), as_moment(end))
