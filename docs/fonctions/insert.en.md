<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `insert`

*[Français](insert.md) · English*

Copy of the array with a value inserted at the given index (negative from the end)

```
insert(source, index, value)
```

**Example**

```jslt
{ "debut": insert($.l, 0, 9), "avant_dernier": insert($.l, -1, 9) }
```

```json
{ "l": [1, 2] }
```

```json
{ "debut": [9, 1, 2], "avant_dernier": [1, 9, 2] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `index` | optional |  |
| `value` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
