<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datediff`

*[Français](datediff.md) · English*

Counts the whole units elapsed between two ISO 8601 dates: second, minute, hour, day, week, month or year, negative when the end precedes the start

```
datediff(start, end, unit)
```

**Example**

```jslt
{ "jours": datediff($.a, $.b, "day") }
```

```json
{ "a": "2026-11-01T00:00:00", "b": "2026-11-11T00:00:00" }
```

```json
{ "jours": 10 }
```

| Parameter | Expected | Note |
|---|---|---|
| `start` | optional |  |
| `end` | optional |  |
| `unit` | optional |  |

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
