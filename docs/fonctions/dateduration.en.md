<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `dateduration`

*[Français](dateduration.md) · English*

Splits the interval between two dates into years, months, days, hours, minutes and seconds

```
dateduration(start, end)
```

**Example**

*The interval broken down into **positive** values; `negative` says which way it goes.*

```jslt
{ "r": dateduration($.a, $.b) }
```

```json
{ "a": "2026-01-01T00:00:00", "b": "2027-03-02T04:05:06" }
```

```json
{ "r": { "negative": false, "years": 1, "months": 2, "days": 1, "hours": 4, "minutes": 5, "seconds": 6 } }
```

| Parameter | Expected | Note |
|---|---|---|
| `start` | optional |  |
| `end` | optional |  |

**Good to know**

- The result carries `negative`: the interval is broken down into positive values, and that flag says which way it goes.

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
