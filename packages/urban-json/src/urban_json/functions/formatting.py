"""``format(valeur, masque, culture)`` — port de ``ExecuteFormat`` (.NET).

Le .NET délègue à ``ToString(mask, culture)`` ; Python n'a ni ces masques ni ces
cultures, on traduit donc le sous-ensemble courant des masques .NET plutôt
que d'exposer la syntaxe Python (décision projet : un template écrit pour le
.NET doit produire le même texte). Couvert :

* nombres — standards ``N F D C P E X G`` (précision optionnelle) et masques
  personnalisés ``0 # . , %`` avec littéraux (``'…'``, ``"…"``, ``\\x``) en
  tête ou en fin de masque ;
* dates — standards ``d D t T f F g G o s u`` et masques personnalisés
  (``yyyy MM MMMM dd dddd HH hh mm ss fff tt`` …). Une chaîne ISO 8601 est une
  date : Newtonsoft (.NET) convertit les chaînes ISO en dates à la lecture.

Hors de ce sous-ensemble : ``JsltError`` explicite, jamais un texte approximatif.
Arrondi « au plus loin de zéro » comme le formatage .NET (pas l'arrondi
bancaire de Python).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from urban_json.errors import JsltError

from ._helpers import is_number, to_text
from .registry import jslt_function

_NNBSP = " "  # séparateur de milliers fr-FR (ICU)
_NBSP = " "

_EN_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
_EN_MONTHS = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]


@dataclass(frozen=True)
class _Culture:
    decimal: str
    group: str
    currency: str  # motif monétaire, `n` = montant
    percent: str  # motif pourcentage, `n` = valeur
    days: list[str]
    days_abbr: list[str]
    months: list[str]
    months_abbr: list[str]
    am: str
    pm: str
    date_sep: str
    short_date: str
    long_date: str
    short_time: str
    long_time: str


def _abbr(names: list[str], size: int = 3) -> list[str]:
    return [n[:size] for n in names]


_INVARIANT = _Culture(
    ".", ",", "¤n", "n %", _EN_DAYS, _abbr(_EN_DAYS), _EN_MONTHS, _abbr(_EN_MONTHS),
    "AM", "PM", "/", "MM/dd/yyyy", "dddd, dd MMMM yyyy", "HH:mm", "HH:mm:ss",
)
_FR_DAYS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
_FR_MONTHS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
              "août", "septembre", "octobre", "novembre", "décembre"]
_DE_DAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
_DE_MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
              "August", "September", "Oktober", "November", "Dezember"]
_ES_DAYS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
_ES_MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
              "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
_IT_DAYS = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
_IT_MONTHS = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
              "agosto", "settembre", "ottobre", "novembre", "dicembre"]

_CULTURES: dict[str, _Culture] = {
    "": _INVARIANT,
    "invariant": _INVARIANT,
    "en-us": _Culture(
        ".", ",", "$n", "n%", _EN_DAYS, _abbr(_EN_DAYS), _EN_MONTHS, _abbr(_EN_MONTHS),
        "AM", "PM", "/", "M/d/yyyy", "dddd, MMMM d, yyyy", "h:mm tt", "h:mm:ss tt",
    ),
    "en-gb": _Culture(
        ".", ",", "£n", "n%", _EN_DAYS, _abbr(_EN_DAYS), _EN_MONTHS, _abbr(_EN_MONTHS),
        "am", "pm", "/", "dd/MM/yyyy", "dddd d MMMM yyyy", "HH:mm", "HH:mm:ss",
    ),
    "fr-fr": _Culture(
        ",", _NNBSP, f"n{_NBSP}€", f"n{_NBSP}%", _FR_DAYS,
        ["lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim."], _FR_MONTHS,
        ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."],
        "", "", "/", "dd/MM/yyyy", "dddd d MMMM yyyy", "HH:mm", "HH:mm:ss",
    ),
    "de-de": _Culture(
        ",", ".", f"n{_NBSP}€", f"n{_NBSP}%", _DE_DAYS, ["Mo.", "Di.", "Mi.", "Do.", "Fr.", "Sa.", "So."],
        _DE_MONTHS, ["Jan.", "Feb.", "März", "Apr.", "Mai", "Juni", "Juli", "Aug.", "Sept.", "Okt.", "Nov.", "Dez."],
        "", "", ".", "dd.MM.yyyy", "dddd, d. MMMM yyyy", "HH:mm", "HH:mm:ss",
    ),
    "es-es": _Culture(
        ",", ".", f"n{_NBSP}€", f"n{_NBSP}%", _ES_DAYS, ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"],
        _ES_MONTHS, ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sept", "oct", "nov", "dic"],
        "a. m.", "p. m.", "/", "dd/MM/yyyy", "dddd, d 'de' MMMM 'de' yyyy", "H:mm", "H:mm:ss",
    ),
    "it-it": _Culture(
        ",", ".", f"n{_NBSP}€", "n%", _IT_DAYS, ["lun", "mar", "mer", "gio", "ven", "sab", "dom"],
        _IT_MONTHS, ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"],
        "", "", "/", "dd/MM/yyyy", "dddd d MMMM yyyy", "HH:mm", "HH:mm:ss",
    ),
}


def _culture(name: Any) -> _Culture:
    key = to_text(name).strip().lower() if name is not None else ""
    culture = _CULTURES.get(key)
    if culture is None:
        supported = ", ".join(sorted(k for k in _CULTURES if k not in ("", "invariant")))
        raise JsltError(f"culture non prise en charge par format : {name!r} (invariante, {supported})")
    return culture


def _unsupported(mask: str, why: str) -> JsltError:
    return JsltError(f"masque de format non pris en charge : {mask!r} ({why})")


# --- nombres ---------------------------------------------------------------------


def _round(value: float, places: int) -> Decimal:
    quantum = Decimal(1).scaleb(-places)
    return Decimal(str(value)).quantize(quantum, rounding=ROUND_HALF_UP)


def _group(digits: str, sep: str) -> str:
    out = []
    while len(digits) > 3:
        out.insert(0, digits[-3:])
        digits = digits[:-3]
    out.insert(0, digits)
    return sep.join(out)


def _fixed(value: float, places: int, culture: _Culture, grouped: bool) -> str:
    rounded = _round(value, places)
    negative = rounded < 0
    text = f"{abs(rounded):f}"
    whole, _, frac = text.partition(".")
    if grouped:
        whole = _group(whole, culture.group)
    body = whole + (culture.decimal + frac if places > 0 else "")
    return ("-" if negative else "") + body


_STANDARD_NUMBER = re.compile(r"^([NnFfDdCcPpEeXxGg])(\d{1,2})?$")


def _standard_number(value: float, letter: str, digits: str | None, mask: str, culture: _Culture) -> str:
    kind = letter.upper()
    precision = int(digits) if digits is not None else None
    if kind == "N":
        return _fixed(value, 2 if precision is None else precision, culture, grouped=True)
    if kind == "F":
        return _fixed(value, 2 if precision is None else precision, culture, grouped=False)
    if kind == "C":
        amount = _fixed(abs(value), 2 if precision is None else precision, culture, grouped=True)
        text = culture.currency.replace("n", amount)
        return "-" + text if value < 0 else text
    if kind == "P":
        amount = _fixed(abs(value) * 100, 2 if precision is None else precision, culture, grouped=True)
        text = culture.percent.replace("n", amount)
        return "-" + text if value < 0 else text
    if kind in ("D", "X"):
        if not isinstance(value, int) and not float(value).is_integer():
            raise _unsupported(mask, f"{kind} n'accepte que des entiers")
        integer = int(value)
        width = precision or 0
        if kind == "D":
            sign = "-" if integer < 0 else ""
            return sign + str(abs(integer)).zfill(width)
        hexa = format(integer & 0xFFFFFFFFFFFFFFFF if integer < 0 else integer, "x").zfill(width)
        return hexa.upper() if letter == "X" else hexa
    if kind == "E":
        places = 6 if precision is None else precision
        mantissa, _, exponent = f"{Decimal(str(value)):.{places}E}".partition("E")
        exp = int(exponent)
        mantissa = mantissa.replace(".", culture.decimal)
        e = "E" if letter == "E" else "e"
        return f"{mantissa}{e}{'+' if exp >= 0 else '-'}{abs(exp):03d}"
    # G : représentation la plus courte (aller-retour), comme .NET Core 3+.
    text = repr(float(value)) if isinstance(value, float) else str(value)
    text = text.removesuffix(".0")
    return text.replace("e", "E").replace(".", culture.decimal)


def _split_literals(mask: str) -> list[tuple[bool, str]]:
    """Découpe un masque en (est_littéral, texte) : '…', "…", \\x."""
    parts: list[tuple[bool, str]] = []
    i = 0
    while i < len(mask):
        ch = mask[i]
        if ch in "'\"":
            end = mask.find(ch, i + 1)
            if end < 0:
                raise _unsupported(mask, "guillemet non fermé")
            parts.append((True, mask[i + 1:end]))
            i = end + 1
        elif ch == "\\" and i + 1 < len(mask):
            parts.append((True, mask[i + 1]))
            i += 2
        else:
            parts.append((False, ch))
            i += 1
    return parts


def _custom_number(value: float, mask: str, culture: _Culture) -> str:
    if ";" in mask:
        raise _unsupported(mask, "sections ';'")
    parts = _split_literals(mask)
    placeholder = [not lit and ch in "0#.," for lit, ch in parts]
    if not any(placeholder):
        return "".join(ch for _, ch in parts)
    first = placeholder.index(True)
    last = len(placeholder) - 1 - placeholder[::-1].index(True)
    if not all(placeholder[first:last + 1]):
        raise _unsupported(mask, "texte au milieu des chiffres")

    def literal(chunk: list[tuple[bool, str]]) -> tuple[str, bool]:
        percent = any(not lit and ch == "%" for lit, ch in chunk)
        return "".join(ch for _, ch in chunk), percent

    prefix, pct_a = literal(parts[:first])
    suffix, pct_b = literal(parts[last + 1:])
    core = "".join(ch for _, ch in parts[first:last + 1])
    if pct_a or pct_b:
        value = value * 100
    int_mask, _, frac_mask = core.partition(".")
    grouped = "," in int_mask.strip(",")
    if int_mask.endswith(","):
        raise _unsupported(mask, "mise à l'échelle par ','")
    int_mask = int_mask.replace(",", "")
    min_int = int_mask.count("0")
    min_frac = len(frac_mask) - len(frac_mask.lstrip("0"))
    max_frac = len(frac_mask)
    rounded = _round(value, max_frac)
    negative = rounded < 0
    whole, _, frac = f"{abs(rounded):f}".partition(".")
    frac = frac.rstrip("0").ljust(min_frac, "0") if max_frac else ""
    whole = whole.lstrip("0").rjust(min_int, "0")
    if grouped and whole:
        whole = _group(whole, culture.group)
    body = whole + (culture.decimal + frac if frac else "")
    return ("-" if negative else "") + prefix + body + suffix


# --- dates ---------------------------------------------------------------------

_DATE_TOKEN = re.compile(r"d{1,4}|f{1,7}|F{1,7}|h{1,2}|H{1,2}|m{1,2}|M{1,4}|s{1,2}|t{1,2}|y{1,5}|K|z{1,3}")


def _custom_date(moment: datetime, mask: str, culture: _Culture) -> str:
    out: list[str] = []
    for literal, chunk in _merge_literals(_split_literals(mask)):
        if literal:
            out.append(chunk)
            continue
        pos = 0
        for match in _DATE_TOKEN.finditer(chunk):
            out.append(_date_separators(chunk[pos:match.start()], culture))
            out.append(_date_token(moment, match.group(0), culture, mask))
            pos = match.end()
        out.append(_date_separators(chunk[pos:], culture))
    return "".join(out)


def _merge_literals(parts: list[tuple[bool, str]]) -> list[tuple[bool, str]]:
    merged: list[tuple[bool, str]] = []
    for literal, ch in parts:
        if merged and merged[-1][0] == literal:
            merged[-1] = (literal, merged[-1][1] + ch)
        else:
            merged.append((literal, ch))
    return merged


def _date_separators(text: str, culture: _Culture) -> str:
    return text.replace("/", culture.date_sep)


def _date_token(moment: datetime, token: str, culture: _Culture, mask: str) -> str:
    kind, size = token[0], len(token)
    if kind == "y":
        # .NET : `y` = année sur 0-99 sans zéro, `yy` sur deux chiffres, au-delà largeur minimale.
        if size <= 2:
            return str(moment.year % 100).zfill(size)
        return str(moment.year).zfill(size)
    if kind == "M":
        if size >= 4:
            return culture.months[moment.month - 1]
        if size == 3:
            return culture.months_abbr[moment.month - 1]
        return str(moment.month).zfill(size)
    if kind == "d":
        if size >= 4:
            return culture.days[moment.weekday()]
        if size == 3:
            return culture.days_abbr[moment.weekday()]
        return str(moment.day).zfill(size)
    if kind == "H":
        return str(moment.hour).zfill(size)
    if kind == "h":
        return str(moment.hour % 12 or 12).zfill(size)
    if kind == "m":
        return str(moment.minute).zfill(size)
    if kind == "s":
        return str(moment.second).zfill(size)
    if kind in "fF":
        digits = f"{moment.microsecond:06d}0"[:size]
        return digits.rstrip("0") if kind == "F" else digits
    if kind == "t":
        designator = culture.am if moment.hour < 12 else culture.pm
        return designator[:1] if size == 1 else designator
    raise _unsupported(mask, f"fuseau '{token}' (dates sans fuseau dans le portage)")


_STANDARD_DATE = {
    "d": lambda c: c.short_date,
    "D": lambda c: c.long_date,
    "t": lambda c: c.short_time,
    "T": lambda c: c.long_time,
    "f": lambda c: f"{c.long_date} {c.short_time}",
    "F": lambda c: f"{c.long_date} {c.long_time}",
    "g": lambda c: f"{c.short_date} {c.short_time}",
    "G": lambda c: f"{c.short_date} {c.long_time}",
    "s": lambda c: "yyyy'-'MM'-'dd'T'HH':'mm':'ss",
    "u": lambda c: "yyyy'-'MM'-'dd' 'HH':'mm':'ss'Z'",
    "o": lambda c: "yyyy'-'MM'-'dd'T'HH':'mm':'ss'.'fffffff",
    "O": lambda c: "yyyy'-'MM'-'dd'T'HH':'mm':'ss'.'fffffff",
}


def _format_date(moment: datetime, mask: str, culture: _Culture) -> str:
    if len(mask) == 1:
        pattern = _STANDARD_DATE.get(mask)
        if pattern is None:
            raise _unsupported(mask, "format de date standard inconnu")
        return _custom_date(moment, pattern(culture), culture)
    return _custom_date(moment, mask, culture)


def _as_date(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.strip())
    except ValueError:
        return None


@jslt_function(
    "format",
    description="Formate un nombre ou une date (chaîne ISO) avec un masque .NET et une culture",
)
def execute_format(ctx: Any, token: Any = None, mask: Any = None, culture: Any = None) -> Any:
    if token is None:
        return None  # le .NET levait une NullReferenceException
    if isinstance(token, bool):
        return to_text(token)
    if isinstance(token, (dict, list)):
        return _json_text(token)
    info = _culture(culture)
    mask_text = "" if mask is None else to_text(mask)
    if is_number(token):
        if not mask_text:
            return _standard_number(token, "G", None, mask_text, info)
        match = _STANDARD_NUMBER.match(mask_text)
        if match:
            return _standard_number(token, match.group(1), match.group(2), mask_text, info)
        if len(mask_text) <= 3 and mask_text[:1].isalpha() and not any(c in mask_text for c in "0#"):
            raise _unsupported(mask_text, "format numérique standard inconnu")
        return _custom_number(token, mask_text, info)
    if isinstance(token, str):
        moment = _as_date(token)
        if moment is not None and mask_text:
            return _format_date(moment, mask_text, info)
    return to_text(token)


def _json_text(value: Any) -> str:
    from ._helpers import stringify

    return stringify(value)
