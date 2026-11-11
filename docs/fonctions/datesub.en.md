<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datesub`

*[Français](datesub.md) · English*

Subtracts a duration from an ISO 8601 date: unit second, minute, hour, day, week, month or year, and a whole number

```
datesub(token, unit, amount)
```

**Example**

```jslt
{ "r": datesub($.d, "day", 1) }
```

```json
{ "d": "2026-03-01T00:00:00" }
```

```json
{ "r": "2026-02-28T00:00:00" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional | the ISO 8601 date to start from |
| `unit` | optional | `second`, `minute`, `hour`, `day`, `week`, `month` or `year` (plural tolerated) |
| `amount` | optional | whole number |

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
