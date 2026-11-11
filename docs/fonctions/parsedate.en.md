<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `parsedate`

*[Français](parsedate.md) · English*

Reads a date from text and returns it in ISO 8601: detection by culture, or an explicit mask (dd/MM/yyyy…), with an optional timezone

```
parsedate(token, culture, mask, timezone)
```

**Example**

```jslt
{ "culture": parsedate($.a, "fr-FR"), "masque": parsedate($.b, "", "dd/MM/yyyy") }
```

```json
{ "a": "11/11/2026", "b": "11/11/2026" }
```

```json
{ "culture": "2026-11-11T00:00:00", "masque": "2026-11-11T00:00:00" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `culture` | optional |  |
| `mask` | optional |  |
| `timezone` | optional |  |

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
