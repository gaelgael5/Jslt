<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `dateendof`

*[Français](dateendof.md) · English*

Last instant of the period holding the date (inclusive bound, to the microsecond)

```
dateendof(token, period)
```

**Example**

```jslt
{ "r": dateendof($.d, "month") }
```

```json
{ "d": "2026-02-10T12:00:00" }
```

```json
{ "r": "2026-02-28T23:59:59.999999" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `period` | optional |  |

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
