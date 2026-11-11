<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `format`

*[Français](format.md) · English*

Formats a number or an ISO date according to a mask (N2, #,##0.00, dd/MM/yyyy…) and a culture

```
format(token, mask, culture)
```

**Examples**

```jslt
{ "nombre": format($.n, "N2", "fr-FR"), "pourcent": format($.p, "P0", "fr-FR") }
```

```json
{ "n": 1234.5, "p": 0.25 }
```

```json
{ "nombre": "1 234,50", "pourcent": "25 %" }
```

```jslt
{ "date": format($.d, "dd/MM/yyyy"), "long": format($.d, "dddd d MMMM yyyy", "fr-FR") }
```

```json
{ "d": "2026-11-11T09:30:00" }
```

```json
{ "date": "11/11/2026", "long": "mercredi 11 novembre 2026" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `mask` | optional |  |
| `culture` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
