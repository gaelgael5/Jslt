# Dates and times — jslt guide

*[Français](dates.md) · English*

[← jslt guide](guide.en.md) · the examples on this page are **run by the test
suite** (`tests/test_guide_examples.py`) as *template → input → output* triples.

---

The engine has no date type: a date is an **ISO 8601 string** — the one
returned by `now()`, `parsedate` and the arithmetic functions, the one `format`
renders. `null` passes through these functions untouched; a value that is not an
ISO date raises rather than silently returning `null`.

**Reading — `parsedate(text, culture, mask, timezone)`.** The last three
arguments are optional, and an empty string means "absent":

| Argument | Empty or absent | Provided |
|---|---|---|
| `culture` | invariant culture: month first (`m/d/y`) | `fr-FR`, `de-DE`, `en-GB`… read `d/m/y`; `en-US` reads `m/d/y` |
| `mask` | detection: ISO 8601, otherwise a numeric date by culture (separators `/ . -`) with optional `HH:mm[:ss]` time | **strict** reading according to the mask |
| `timezone` | the date keeps what it carries: naive if the input is naive, its offset otherwise | **qualifies** a naive date, **converts** a date that already carries an offset |

A timezone is written as an IANA name (`Europe/Paris`), as `UTC` / `Z`, or as a
fixed offset (`+02:00`, `-0500`); an unknown name raises. Qualifying rather than
shifting is what a local time calls for: `2026-07-10T08:30:00` in
`Europe/Paris` stays 8:30, with the summer offset `+02:00`.

```jslt
{ "auto": parsedate($.a, "en-US"), "mask": parsedate($.b, "en-US", "MM/dd/yyyy h:mm tt"), "ny": parsedate($.c, "", "", "America/New_York") }
```
```json
{ "a": "10/22/2026", "b": "10/22/2026 2:05 PM", "c": "2026-07-04T16:00:00Z" }
```
```json
{ "auto": "2026-10-22T00:00:00", "mask": "2026-10-22T14:05:00", "ny": "2026-07-04T12:00:00-04:00" }
```

## Date masks

The reading mask and the writing one (`format`) share **one** vocabulary: what is
written can be read back.

| Token | Reads | Example |
|---|---|---|
| `yyyy` | four-digit year | `2026` |
| `yy` | two-digit year: `00`-`49` → 20xx, `50`-`99` → 19xx | `26` → 2026 |
| `MM` / `M` | numeric month | `10` |
| `MMMM` / `MMM` | month name, full or abbreviated, per culture | `October` / `Oct` |
| `dd` / `d` | day of month | `22` |
| `dddd` / `ddd` | day name — read so the mask matches, then ignored | `Thursday` |
| `HH` / `H` | 24-hour clock | `14` |
| `hh` / `h` | 12-hour clock; requires `t` or `tt` | `02` |
| `mm` / `m` | minutes | `05` |
| `ss` / `s` | seconds | `09` |
| `f` to `fffffff` | fractional seconds, as many digits as `f` | `250` |
| `F` to `FFFFFFF` | same, but the digits are optional | |
| `tt` / `t` | the culture's AM/PM designator, full or first letter | `PM` / `P` |
| `zzz` / `zz` / `z` | UTC offset | `+01:00` |
| `K` | `Z`, an offset, or nothing | `Z` |
| `'…'` `"…"` `\x` | literal, shielded from interpretation | `'T'` |
| `/` | the **culture's** date separator (`.` in `de-DE`) | `/` |

Widths are **strict**: `dd` requires two digits, `d` accepts one or two. A
tolerant width would let `1/2/26` pass for a date under the `dd/MM/yyyy` mask,
and that is rarely what one wants when imposing a mask. A **single-letter** mask is one of `format`'s standard masks
(`d D t T f F g G s u o`), resolved per culture: `parsedate($.x, "fr-FR", "d")`
reads `22/10/2026`. A component the mask does not carry takes its value from the
Unix epoch (`1970-01-01`, `00:00:00`) — not from "today", so that the same
template does not change result depending on the day it runs. Text that does not
match the mask raises.

**Arithmetic — `dateadd(date, unit, n)` and `datesub(date, unit, n)`.** Units:
`second`, `minute`, `hour`, `day`, `week`, `month`, `year` (plural and case are
tolerated). `n` is an **integer**, negative allowed: `datesub(d, u, n)` is
exactly `dateadd(d, u, -n)`. `month` and `year` are calendar-based and **clamp**
the day to the last day of the target month — January 31 + 1 month gives
February 28, the 29th in a leap year. The input's UTC offset is preserved.

**Measuring — `datediff(start, end, unit)`.** Counts the **whole** units
elapsed, with the same units, and returns a negative number when `end` precedes
`start`. Truncation goes **toward zero**: 36 hours make 1 day, 12 hours make 0,
and -36 hours make -1. `month` and `year` are calendar-based — a month is only
whole once the day and time of `end` have caught up with those of `start`. Worth
knowing: `datediff` is not the exact inverse of `dateadd` for those two units,
since `dateadd` clamps the day on short months (from January 31, `dateadd` of
one month gives February 28, which `datediff` counts as 0 whole months).
Comparing a date with a timezone to one without raises, rather than assuming one.

```jslt
{ "days": datediff($.a, $.b, "day"), "months": datediff($.a, $.b, "month"), "back": datediff($.b, $.a, "day") }
```
```json
{ "a": "2026-11-10T08:30:00", "b": "2026-12-25T00:00:00" }
```
```json
{ "days": 44, "months": 1, "back": -44 }
```

**Extraction — `datepart(date, part)`.** Parts: `year`, `month`, `day`,
`dayofweek`, `hour`, `minute`, `second`, always returned as a number.
`dayofweek` numbers the week from **Sunday = 0** (Saturday = 6).

```jslt
{ "in3months": dateadd($.d, "month", 3), "dayBefore": datesub($.d, "day", 1), "year": datepart($.d, "year"), "weekday": datepart($.d, "dayofweek") }
```
```json
{ "d": "2026-11-10T08:30:00" }
```
```json
{ "in3months": "2027-02-10T08:30:00", "dayBefore": "2026-11-09T08:30:00", "year": 2026, "weekday": 2 }
```

Day clamping, and chaining with `format` for display:

```jslt
{ "clamped": dateadd($.d, "month", 1), "readable": format(dateadd($.d, "month", 1), "MMMM d, yyyy", "en-US") }
```
```json
{ "d": "2026-01-31T00:00:00" }
```
```json
{ "clamped": "2026-02-28T00:00:00", "readable": "February 28, 2026" }
```

---

## Extra parts and period bounds

`datepart` now knows `year`, `quarter`, `month`, `week`, `day`, `dayofyear`,
`dayofweek`, `hour`, `minute`, `second` and `millisecond`. `week` is the **ISO**
week: 1 January sometimes belongs to week 52 or 53 of the previous year, and that
is the definition expected in Europe. `dayofweek`, on the other hand, keeps
numbers from Sunday = 0.

`datestartof(date, period)` and `dateendof(date, period)` bound a period: `year`,
`quarter`, `month`, `week`, `day`, `hour`, `minute`. The end is **inclusive**, to
the microsecond (`23:59:59.999999`), because that is what a `<=` filter expects.
The input's UTC offset is preserved.

The week starts on **Monday** (ISO). Yes, that coexists with a `dayofweek` where
Sunday is 0: the two conventions coexist,
the bound follows European usage. Both choices are deliberate.

```jslt
{
  "quarter": datepart($.d, "quarter"),
  "week": datepart($.d, "week"),
  "day_of_year": datepart($.d, "dayofyear"),
  "month_start": datestartof($.d, "month"),
  "quarter_end": dateendof($.d, "quarter")
}
```

```json
{ "d": "2026-11-15T08:30:05.123456" }
```

```json
{
  "quarter": 4,
  "week": 46,
  "day_of_year": 319,
  "month_start": "2026-11-01T00:00:00",
  "quarter_end": "2026-12-31T23:59:59.999999"
}
```

## Business days (`weekday`)

`dateadd`, `datesub` and `datediff` accept the `weekday` unit: Saturdays and
Sundays are skipped. From a Friday, `dateadd(d, "weekday", 1)` lands on Monday.

**No public-holiday calendar is applied.** It depends on the country, the year
and sometimes the company: embedding one would give wrong, silent results outside
its scope. For holidays, subtract them explicitly in the template.

```jslt
{
  "delivery": dateadd($.order, "weekday", 3),
  "business_days": datediff($.order, $.due, "weekday")
}
```

```json
{ "order": "2026-11-13T09:00:00", "due": "2026-11-20T09:00:00" }
```

```json
{ "delivery": "2026-11-18T09:00:00", "business_days": 5 }
```

## Explicit timezone, today and duration

`datezone(date, zone)` does what the detour
`parsedate(date, "", "", "Europe/Paris")` did: it **assigns** the zone to a naive
date and **converts** a date that already carries an offset. A date already read
no longer has to go back through a reading function to change zone.

`today()` returns the current day at **midnight** (`today(true)` in UTC): `now()`
carries the time, which prevents comparing two days without truncating by hand.

`dateduration(start, end)` breaks the interval down into years, months, days,
hours, minutes and seconds, with a `negative` flag. An object, not a sentence
like "3 days ago": the wording depends on language and context, the template can
do it, and the engine carries no phrase catalogue.

```jslt
{
  "paris": datezone($.utc, "Europe/Paris"),
  "duration": dateduration($.start, $.end)
}
```

```json
{ "utc": "2026-11-15T08:30:00+00:00", "start": "2026-01-31T08:00:00", "end": "2027-03-02T09:30:10" }
```

```json
{
  "paris": "2026-11-15T09:30:00+01:00",
  "duration": { "negative": false, "years": 1, "months": 1, "days": 2, "hours": 1, "minutes": 30, "seconds": 10 }
}
```

---

**See also**: [writing a date](texte.en.md#formatting-format) with `format`,
and `now()` in the [cheat sheet](guide.en.md#cheat-sheet).

---

[← jslt guide](guide.en.md)
