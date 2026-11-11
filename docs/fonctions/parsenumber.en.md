<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `parsenumber`

*[Français](parsenumber.md) · English*

Reads a number written as text according to a culture (1 234,56 in fr-FR)

```
parsenumber(token, culture)
```

**Example**

```jslt
{ "r": parsenumber($.t, "fr-FR") }
```

```json
{ "t": "1 234,56" }
```

```json
{ "r": 1234.56 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `culture` | optional |  |

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
