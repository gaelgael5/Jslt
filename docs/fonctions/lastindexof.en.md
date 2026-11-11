<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `lastindexof`

*[Français](lastindexof.md) · English*

Position (from 0) of the last occurrence in a text or an array, -1 when absent

```
lastindexof(token, txt)
```

**Example**

```jslt
{ "r": lastindexof($.t, "o") }
```

```json
{ "t": "bonjour" }
```

```json
{ "r": 4 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `txt` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
