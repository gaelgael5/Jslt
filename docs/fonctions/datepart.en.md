<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datepart`

*[Français](datepart.md) · English*

Extracts a whole component from an ISO 8601 date: year, month, day, dayofweek (Sunday = 0), hour, minute or second

```
datepart(token, part)
```

**Example**

*`dayofweek` counts from **Sunday = 0**: 11 November 2026 is a Wednesday, hence 3.*

```jslt
{ "annee": datepart($.d, "year"), "trimestre": datepart($.d, "quarter"), "jour_semaine": datepart($.d, "dayofweek") }
```

```json
{ "d": "2026-11-11T09:30:00" }
```

```json
{ "annee": 2026, "trimestre": 4, "jour_semaine": 3 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional | the ISO 8601 date to break down |
| `part` | optional | `year`, `quarter`, `month`, `day`, `dayofweek`, `dayofyear`, `week`, `hour`, `minute` or `second` |

**Good to know**

- `dayofweek` numbers from **Sunday = 0** (Saturday = 6), whereas `datestartof(…, "week")` starts on **Monday** (ISO). Both conventions coexist: the first names a day, the second bounds a week.
- Available parts: `year`, `quarter`, `month`, `day`, `dayofweek`, `dayofyear`, `week`, `hour`, `minute`, `second`.

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
