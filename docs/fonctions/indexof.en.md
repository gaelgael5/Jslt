<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `indexof`

*[Français](indexof.md) · English*

Position (from 0) of the first occurrence in a text or an array, -1 when absent

```
indexof(token, txt)
```

**Example**

```jslt
{ "texte": indexof($.t, "o"), "tableau": indexof($.l, "b") }
```

```json
{ "t": "bonjour", "l": ["a", "b", "c"] }
```

```json
{ "texte": 1, "tableau": 1 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `txt` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
