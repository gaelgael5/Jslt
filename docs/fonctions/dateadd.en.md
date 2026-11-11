<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `dateadd`

*[Français](dateadd.md) · English*

Adds a duration to an ISO 8601 date: unit second, minute, hour, day, week, month or year, and a whole number (negative to subtract)

```
dateadd(token, unit, amount)
```

**Examples**

*Adding, and subtracting with a negative amount.*

```jslt
{ "dans_deux_mois": dateadd($.d, "month", 2), "hier": dateadd($.d, "day", -1) }
```

```json
{ "d": "2026-01-15T00:00:00" }
```

```json
{ "dans_deux_mois": "2026-03-15T00:00:00", "hier": "2026-01-14T00:00:00" }
```

*`month` is a **calendar** unit: 31 January + 1 month gives 28 February, clamped on the short month — not 3 March.*

```jslt
{ "borne": dateadd($.d, "month", 1) }
```

```json
{ "d": "2026-01-31T00:00:00" }
```

```json
{ "borne": "2026-02-28T00:00:00" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional | the ISO 8601 date to start from |
| `unit` | optional | `second`, `minute`, `hour`, `day`, `week`, `month` or `year` (plural tolerated) |
| `amount` | optional | whole number, negative to subtract |

**Good to know**

- `month` and `year` are **calendar** units: the day is **clamped** on short months, so 31 January + 1 month gives 28 February, not 3 March.
- Consequence: `dateadd` and `datediff` are **not** exact inverses of each other on those two units.

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
