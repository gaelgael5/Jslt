<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datepart`

*[Français](datepart.md) · English*

Extracts a whole component from an ISO 8601 date: year, month, day, dayofweek (Sunday = 0), hour, minute or second

```
datepart(token, part)
```

**Example**

```jslt
{ "annee": datepart($.d, "year"), "jour_semaine": datepart($.d, "dayofweek") }
```

```json
{ "d": "2026-11-11T09:30:00" }
```

```json
{ "annee": 2026, "jour_semaine": 3 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `part` | optional |  |

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
