<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `capitalize`

*[Français](capitalize.md) · English*

Upper-cases the first letter only, leaving the rest untouched

```
capitalize(token)
```

**Example**

*The first letter **only**; `titlecase` upper-cases every initial.*

```jslt
{ "cap": capitalize($.t), "titre": titlecase($.t) }
```

```json
{ "t": "bonjour le MONDE" }
```

```json
{ "cap": "Bonjour le MONDE", "titre": "Bonjour Le MONDE" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
