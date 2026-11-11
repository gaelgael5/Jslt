<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `dateendof`

*[Français](dateendof.md) · English*

Last instant of the period holding the date (inclusive bound, to the microsecond)

```
dateendof(token, period)
```

**Example**

*An **inclusive** bound: the last microsecond of the period, so that a `<=` filter catches the whole day (or the whole month).*

```jslt
{ "mois": dateendof($.d, "month"), "jour": dateendof($.d, "day") }
```

```json
{ "d": "2026-02-10T12:00:00" }
```

```json
{ "mois": "2026-02-28T23:59:59.999999", "jour": "2026-02-10T23:59:59.999999" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional | the ISO 8601 date to carry to the end of its period |
| `period` | optional | `year`, `quarter`, `month`, `week`, `day`, `hour` or `minute` |

**Good to know**

- The bound is **inclusive**, to the microsecond: the end of a day is `23:59:59.999999`, not the start of the next one. So a `<=` filter catches the whole day.

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
