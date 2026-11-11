<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `dateadd`

*[Français](dateadd.md) · English*

Adds a duration to an ISO 8601 date: unit second, minute, hour, day, week, month or year, and a whole number (negative to subtract)

```
dateadd(token, unit, amount)
```

**Example**

```jslt
{ "r": dateadd($.d, "month", 2) }
```

```json
{ "d": "2026-01-31T00:00:00" }
```

```json
{ "r": "2026-03-31T00:00:00" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `unit` | optional |  |
| `amount` | optional |  |

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
