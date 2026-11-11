<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `slice`

*[Français](slice.md) · English*

Slice of an array from start to end excluded (negative indices from the end)

```
slice(source, start, end)
```

**Example**

*End excluded, negative indices from the end, over-wide bounds tolerated.*

```jslt
{ "milieu": slice($.l, 1, 3), "fin": slice($.l, -2), "trop_loin": slice($.l, 9) }
```

```json
{ "l": [1, 2, 3, 4, 5] }
```

```json
{ "milieu": [2, 3], "fin": [4, 5], "trop_loin": [] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `start` | optional |  |
| `end` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
