<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `difference`

*[Français](difference.md) · English*

Elements of the left array absent from the right one, deduplicated

```
difference(left, right)
```

**Example**

```jslt
{ "r": difference($.a, $.b) }
```

```json
{ "a": [1, 2, 3], "b": [2] }
```

```json
{ "r": [1, 3] }
```

| Parameter | Expected | Note |
|---|---|---|
| `left` | optional |  |
| `right` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
