<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datestartof`

*[Français](datestartof.md) · English*

First instant of the period holding the date: year, quarter, month, week (Monday), day, hour or minute

```
datestartof(token, period)
```

**Example**

```jslt
{ "r": datestartof($.d, "week") }
```

```json
{ "d": "2026-11-11T09:30:00" }
```

```json
{ "r": "2026-11-09T00:00:00" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `period` | optional |  |

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
