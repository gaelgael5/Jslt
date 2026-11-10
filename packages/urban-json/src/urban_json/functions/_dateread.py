"""Lecture d'une date : détection automatique, ou **masque .NET** — l'inverse de
l'écriture faite par ``format``.

Tout ce qui transforme du texte en ``datetime`` vit ici (détection, masque,
fuseau) ; :mod:`.dates` garde les fonctions exposées et le calcul.

Le même vocabulaire de masque sert donc à lire et à écrire : ``yyyy MM dd HH mm
ss fff tt MMMM dddd zzz K``, littéraux ``'…'`` / ``"…"`` / ``\\x``, et masques
standard d'une lettre (``d D t T f F g G s u o``). C'est une décision du portage
(un seul vocabulaire à apprendre, et un aller-retour ``format`` →
``parsedate`` cohérent) : le tokeniseur et les tables de culture sont importés
de :mod:`.formatting` plutôt que redéfinis ici, pour qu'ils ne divergent pas.

Largeurs **strictes** comme ``DateTime.ParseExact`` : ``dd`` exige deux
chiffres, ``d`` en accepte un ou deux. Un masque non respecté lève une
``JsltError`` plutôt que de rendre une date approximative.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from typing import Any

from urban_json.errors import JsltError

from ._helpers import to_text
from .formatting import (
    _DATE_TOKEN,
    _STANDARD_DATE,
    _Culture,
    _culture,
    _date_separators,
    _merge_literals,
    _split_literals,
)

# Date retenue quand le masque ne porte pas la composante : l'époque Unix.
# Écart volontaire vs .NET, qui complète avec « aujourd'hui » — ce qui rendrait
# le résultat d'un même template dépendant du jour d'exécution.
_DEFAULT_DATE = (1970, 1, 1)


def full_year(year: int, digits: int) -> int:
    """Année sur deux chiffres : fenêtre .NET par défaut (``TwoDigitYearMax`` = 2049)."""
    if digits > 2:
        return year
    return 2000 + year if year <= 49 else 1900 + year


def parse_with_mask(text: str, mask: str, culture_name: Any) -> datetime:
    """Lit ``text`` selon ``mask`` (vocabulaire .NET) et rend un ``datetime``."""
    culture = _culture(culture_name)
    pattern = mask
    if len(mask) == 1:
        standard = _STANDARD_DATE.get(mask)
        if standard is None:
            raise JsltError(f"masque de date non pris en charge : {mask!r} (standard inconnu)")
        pattern = standard(culture)
    regex, kinds = _compile(pattern, culture, mask)
    match = regex.fullmatch(text)
    if match is None:
        raise JsltError(f"date {text!r} non conforme au masque {mask!r}")
    return _assemble(match, kinds, culture, text, mask)


def _compile(pattern: str, culture: _Culture, mask: str) -> tuple[re.Pattern[str], list[str]]:
    """Traduit le masque en expression régulière, et liste le jeton de chaque groupe."""
    parts: list[str] = []
    kinds: list[str] = []
    for literal, chunk in _merge_literals(_split_literals(pattern)):
        if literal:
            parts.append(re.escape(chunk))
            continue
        pos = 0
        for match in _DATE_TOKEN.finditer(chunk):
            parts.append(re.escape(_date_separators(chunk[pos:match.start()], culture)))
            token = match.group(0)
            parts.append(f"(?P<t{len(kinds)}>{_token_regex(token, culture, mask)})")
            kinds.append(token)
            pos = match.end()
        parts.append(re.escape(_date_separators(chunk[pos:], culture)))
    # IGNORECASE : .NET lit « OCTOBRE » comme « octobre » (ParseExact est
    # insensible à la casse des noms de mois et de jours).
    return re.compile("".join(parts), re.IGNORECASE), kinds


def _names(values: list[str]) -> str:
    """Alternation des noms, du plus long au plus court — sinon « mar » masquerait « mars »."""
    return "|".join(re.escape(v) for v in sorted(values, key=len, reverse=True))


def _digits(size: int, exact: bool) -> str:
    return rf"\d{{{size}}}" if exact else r"\d{1,2}"


def _token_regex(token: str, culture: _Culture, mask: str) -> str:
    kind, size = token[0], len(token)
    if kind == "y":
        return _digits(size, size != 1)
    if kind == "M":
        if size >= 4:
            return _names(culture.months)
        if size == 3:
            return _names(culture.months_abbr)
        return _digits(size, size == 2)
    if kind == "d":
        if size >= 4:
            return _names(culture.days)
        if size == 3:
            return _names(culture.days_abbr)
        return _digits(size, size == 2)
    if kind in "Hhms":
        return _digits(size, size == 2)
    if kind == "f":
        return rf"\d{{{size}}}"
    if kind == "F":
        return rf"\d{{0,{size}}}"
    if kind == "t":
        if not culture.am and not culture.pm:
            raise JsltError(
                f"masque {mask!r} : la culture ne connaît pas AM/PM, utiliser 'HH' plutôt que 'h'/'tt'"
            )
        designators = [culture.am, culture.pm]
        return _names(designators if size > 1 else [d[:1] for d in designators])
    if kind == "z":
        if size >= 3:
            return r"[+-]\d{2}:\d{2}"
        return rf"[+-]\d{{{size}}}" if size == 2 else r"[+-]\d{1,2}"
    if kind == "K":
        return r"Z|[+-]\d{2}:\d{2}|"
    raise JsltError(f"masque de date non pris en charge : {mask!r} (jeton {token!r} inconnu)")


def _assemble(
    match: re.Match[str], kinds: list[str], culture: _Culture, text: str, mask: str
) -> datetime:
    year, month, day = _DEFAULT_DATE
    hour = minute = second = micro = 0
    half: int | None = None  # heure lue en 12 h, à redresser avec le désignateur
    pm: bool | None = None
    offset: timezone | None = None
    for index, token in enumerate(kinds):
        raw = match.group(f"t{index}")
        kind, size = token[0], len(token)
        if kind == "y":
            year = full_year(int(raw), size)
        elif kind == "M":
            month = _name_index(raw, culture.months, culture.months_abbr) if size >= 3 else int(raw)
        elif kind == "d":
            # ddd/dddd : le nom du jour n'apporte aucune composante, il est lu
            # (pour que le masque colle) puis ignoré, comme en .NET.
            if size <= 2:
                day = int(raw)
        elif kind == "H":
            hour = int(raw)
        elif kind == "h":
            half = int(raw)
        elif kind == "m":
            minute = int(raw)
        elif kind == "s":
            second = int(raw)
        elif kind in "fF":
            micro = int(raw.ljust(6, "0")[:6]) if raw else 0
        elif kind == "t":
            pm = raw.lower().startswith(culture.pm[: len(raw)].lower()) if culture.pm else False
        elif kind in "zK":
            offset = _offset(raw)
    if half is not None:
        hour = _hour12(half, pm, mask)
    try:
        return datetime(year, month, day, hour, minute, second, micro, tzinfo=offset)
    except ValueError as exc:
        raise JsltError(f"date invalide : {text!r} ({exc})") from exc


def _hour12(hour: int, pm: bool | None, mask: str) -> int:
    if pm is None:
        raise JsltError(f"masque {mask!r} : 'h' (12 h) sans désignateur 't'/'tt'")
    if hour == 12:
        return 12 if pm else 0
    return hour + 12 if pm else hour


def _name_index(raw: str, names: list[str], abbreviated: list[str]) -> int:
    low = raw.lower()
    for table in (names, abbreviated):
        for position, name in enumerate(table):
            if name.lower() == low:
                return position + 1
    raise JsltError(f"nom de mois inconnu : {raw!r}")


def _offset(raw: str) -> timezone | None:
    """Décalage d'un jeton ``z``/``zz``/``zzz``/``K`` ; ``None`` si le jeton est vide."""
    if not raw or raw.upper() == "Z":
        return timezone.utc if raw else None
    sign = -1 if raw[0] == "-" else 1
    body = raw[1:]
    hours, _, minutes = body.partition(":")
    return timezone(sign * timedelta(hours=int(hours), minutes=int(minutes or 0)))


# --- détection, sans masque ---------------------------------------------------

# Cultures qui lisent « 10/22/2026 » mois d'abord (comme la culture invariante
# .NET) ; toutes les autres lisent jour d'abord (fr-FR, de-DE, en-GB…).
_MONTH_FIRST = {"", "invariant", "en", "en-us"}
_NUMERIC_DATE = re.compile(
    r"^(\d{1,4})[./-](\d{1,2})[./-](\d{1,4})"
    r"(?:[ T](\d{1,2}):(\d{2})(?::(\d{2}))?)?$"
)
_FIXED_OFFSET = re.compile(r"^([+-])(\d{1,2}):?(\d{2})?$")


def detect_date(text: str, culture: Any) -> datetime:
    """Détection sans masque : ISO 8601, puis dates numériques selon la culture."""
    iso = from_iso(text)
    if iso is not None:
        return iso
    match = _NUMERIC_DATE.match(text)
    if match is None:
        raise JsltError(f"date illisible : {text!r}")
    first, second, third, hour, minute, sec = match.groups()
    if len(first) == 4:
        year, month, day = int(first), int(second), int(third)
    else:
        year = full_year(int(third), len(third))
        month_first = to_text(culture).strip().lower() in _MONTH_FIRST
        month, day = (int(first), int(second)) if month_first else (int(second), int(first))
    try:
        # Sans fuseau, volontairement : DateTime.Parse .NET rend une date « Unspecified ».
        return datetime(year, month, day, int(hour or 0), int(minute or 0), int(sec or 0))  # noqa: DTZ001
    except ValueError as exc:
        raise JsltError(f"date invalide : {text!r} ({exc})") from exc


def from_iso(text: str) -> datetime | None:
    # Le 'Z' final n'est accepté par fromisoformat qu'à partir de Python 3.11 ;
    # le paquet supporte 3.9, on le normalise donc nous-mêmes.
    candidate = f"{text[:-1]}+00:00" if text.endswith(("Z", "z")) else text
    try:
        return datetime.fromisoformat(candidate)
    except ValueError:
        return None


def as_moment(value: Any) -> datetime:
    if isinstance(value, str):
        moment = from_iso(value.strip())
        if moment is not None:
            return moment
    raise JsltError(f"date ISO 8601 attendue, reçu : {value!r}")


def in_zone(moment: datetime, zone_text: str) -> datetime:
    zone = resolve_zone(zone_text)
    if moment.tzinfo is None:
        # Date sans décalage : le fuseau la **qualifie** (l'heure lue est l'heure
        # locale de ce fuseau), il ne la décale pas. zoneinfo choisit l'offset
        # correct pour ce jour-là, heure d'été comprise.
        return moment.replace(tzinfo=zone)
    return moment.astimezone(zone)


def resolve_zone(text: str):
    if text.upper() in ("Z", "UTC"):
        return timezone.utc
    fixed = _FIXED_OFFSET.match(text)
    if fixed:
        sign, hours, minutes = fixed.groups()
        delta = timedelta(hours=int(hours), minutes=int(minutes or 0))
        return timezone(-delta if sign == "-" else delta)
    try:
        from zoneinfo import ZoneInfo

        return ZoneInfo(text)
    except (ImportError, ValueError, KeyError) as exc:
        # Nom IANA inconnu — ou base de fuseaux absente du système (Windows sans
        # le paquet `tzdata`) : on le dit, plutôt que de replier sur UTC.
        raise JsltError(
            f"fuseau horaire inconnu : {text!r} (nom IANA comme 'Europe/Paris', "
            f"'UTC', ou décalage fixe '+02:00')"
        ) from exc
