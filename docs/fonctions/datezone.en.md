<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datezone`

*[Français](datezone.md) · English*

Attaches a timezone to a date without offset, or converts a date that already carries one

```
datezone(token, zone)
```

**Example**

```jslt
{ "r": datezone($.d, "Europe/Paris") }
```

```json
{ "d": "2026-11-11T09:30:00" }
```

```json
{ "r": "2026-11-11T09:30:00+01:00" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `zone` | optional |  |

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
