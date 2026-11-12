<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `removeat`

*[Français](removeat.md) · English*

Copy of the array without the element at the given index (negative from the end)

```
removeat(source, index)
```

**Example**

*An out-of-range index returns the copy **unchanged**, it does not raise.*

```jslt
{ "sans_le_second": removeat($.l, 1), "dernier": removeat($.l, -1), "hors_bornes": removeat($.l, 9) }
```

```json
{ "l": [1, 2, 3] }
```

```json
{ "sans_le_second": [1, 3], "dernier": [1, 2], "hors_bornes": [1, 2, 3] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `index` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
