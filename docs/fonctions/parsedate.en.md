<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `parsedate`

*[Français](parsedate.md) · English*

Reads a date from text and returns it in ISO 8601: detection by culture, or an explicit mask (dd/MM/yyyy…), with an optional timezone

```
parsedate(token, culture, mask, timezone)
```

**Examples**

*An **ISO 8601** date reads with nothing: no culture, no mask.*

```jslt
{ "d": parsedate($.t) }
```

```json
{ "t": "2026-11-11T09:30:00Z" }
```

```json
{ "d": "2026-11-11T09:30:00+00:00" }
```

*With no mask, the **culture** decides the order: month first in `en-US`, day first everywhere else. The same text gives two dates.*

```jslt
{ "us": parsedate($.t, "en-US"), "gb": parsedate($.t, "en-GB") }
```

```json
{ "t": "03/04/2026" }
```

```json
{ "us": "2026-03-04T00:00:00", "gb": "2026-04-03T00:00:00" }
```

*A month **spelled out** requires a mask: automatic detection only reads numeric forms and ISO. `MMMM` takes the culture's names.*

```jslt
{ "en": parsedate($.a, "en-US", "MMMM d, yyyy"), "fr": parsedate($.b, "fr-FR", "d MMMM yyyy") }
```

```json
{ "a": "November 11, 2026", "b": "11 novembre 2026" }
```

```json
{ "en": "2026-11-11T00:00:00", "fr": "2026-11-11T00:00:00" }
```

*Abbreviations (`MMM`, `ddd`), and a 12-hour clock: `h` **requires** `tt`, the culture's AM/PM designator.*

```jslt
{ "jour": parsedate($.a, "en-GB", "ddd, d MMM yyyy"), "heure": parsedate($.b, "en-US", "MM/dd/yyyy h:mm tt") }
```

```json
{ "a": "Wed, 11 Nov 2026", "b": "11/11/2026 2:05 PM" }
```

```json
{ "jour": "2026-11-11T00:00:00", "heure": "2026-11-11T14:05:00" }
```

*Without separators, a mask is enough. And a **single-letter** mask is a standard mask, resolved per culture (`d` = short date).*

```jslt
{ "compact": parsedate($.a, "", "yyyyMMdd"), "court": parsedate($.b, "en-US", "d") }
```

```json
{ "a": "20261111", "b": "11/11/2026" }
```

```json
{ "compact": "2026-11-11T00:00:00", "court": "2026-11-11T00:00:00" }
```

*A component the mask does not carry comes from the **Unix epoch**, never from today: the same template returns the same thing tomorrow.*

```jslt
{ "heure_seule": parsedate($.t, "", "HH:mm") }
```

```json
{ "t": "11:30" }
```

```json
{ "heure_seule": "1970-01-01T11:30:00" }
```

*The 4th argument **qualifies** a date without offset (it is given a timezone) and **converts** one that already carries an offset.*

```jslt
{ "qualifie": parsedate($.a, "", "", "Europe/Paris"), "convertit": parsedate($.b, "", "", "UTC") }
```

```json
{ "a": "2026-11-11", "b": "2026-11-11T09:30:00+01:00" }
```

```json
{ "qualifie": "2026-11-11T00:00:00+01:00", "convertit": "2026-11-11T08:30:00+00:00" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional | the text to read; `null` gives `null` |
| `culture` | optional | decides the day/month order without a mask, and the names (months, days, AM/PM) with one: `en-US`, `en-GB`, `fr-FR`, `de-DE`, `es-ES`, `it-IT`, or empty for the invariant one (English) |
| `mask` | optional | explicit mask (`dd/MM/yyyy`, `MMMM d, yyyy`…), **required** as soon as a month or a day is spelled out |
| `timezone` | optional | IANA name (`Europe/Paris`), `UTC`/`Z`, or a fixed offset (`+02:00`): qualifies a naive date, converts one that already carries an offset |

**Good to know**

- **With no mask, only numeric forms and ISO 8601 are recognised.** `parsedate($.t, "en-US")` on "November 11, 2026" raises `date illisible`: a month or a day **spelled out** requires a mask (`MMMM`, `MMM`, `dddd`, `ddd`).
- The full token vocabulary — and what each one reads — is in [Date masks](../dates.en.md#date-masks). It is **shared** with `format`: what is written can be read back.
- Widths are **strict**: `dd` requires two digits, `d` accepts one or two. So `1/2/26` does not match `dd/MM/yyyy`, and raises.
- `ddd` / `dddd` (the day name) are **read then ignored**: they are there so the mask matches the text, not to decide the date.
- The month and day names, the date separator and the AM/PM designator come from the **culture** (2nd argument): it decides whether `MMMM` reads "November" or "novembre". Cultures: empty (invariant, English), `en-US`, `en-GB`, `fr-FR`, `de-DE`, `es-ES`, `it-IT`.
- `null` gives `null`. Text that is not a date **raises** rather than returning a wrong date or "today": the fault shows where it is.

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
