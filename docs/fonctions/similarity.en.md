<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `similarity`

*[Français](similarity.md) · English*

Closeness of two texts between 0 (all differs) and 1 (identical)

```
similarity(left, right)
```

**Example**

```jslt
{ "r": round(similarity($.a, $.b), 2) }
```

```json
{ "a": "Durand", "b": "Durrand" }
```

```json
{ "r": 0.86 }
```

| Parameter | Expected | Note |
|---|---|---|
| `left` | optional |  |
| `right` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
