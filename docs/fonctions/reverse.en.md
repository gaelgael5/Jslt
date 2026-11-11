<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `reverse`

*[Français](reverse.md) · English*

Reverses the order of an array or of a text, without modifying the source

```
reverse(source)
```

**Example**

```jslt
{ "tableau": reverse($.l), "texte": reverse($.t) }
```

```json
{ "l": [1, 2, 3], "t": "abc" }
```

```json
{ "tableau": [3, 2, 1], "texte": "cba" }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
