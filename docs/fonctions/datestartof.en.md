<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datestartof`

*[Français](datestartof.md) · English*

First instant of the period holding the date: year, quarter, month, week (Monday), day, hour or minute

```
datestartof(token, period)
```

**Example**

*The week starts on **Monday**: a Wednesday is brought back to the Monday before it, at midnight.*

```jslt
{ "semaine": datestartof($.d, "week"), "mois": datestartof($.d, "month") }
```

```json
{ "d": "2026-11-11T09:30:00" }
```

```json
{ "semaine": "2026-11-09T00:00:00", "mois": "2026-11-01T00:00:00" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional | the ISO 8601 date to bring back to the start of its period |
| `period` | optional | `year`, `quarter`, `month`, `week` (Monday), `day`, `hour` or `minute` |

**Good to know**

- The week starts on **Monday** (ISO). Periods: `year`, `quarter`, `month`, `week`, `day`, `hour`, `minute`.

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
