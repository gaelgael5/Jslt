<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `window`

*[Français](window.md) · English*

Sliding windows of size consecutive elements (empty when the array is shorter)

```
window(source, size)
```

**Example**

```jslt
{ "r": window($.l, 2) }
```

```json
{ "l": [1, 2, 3] }
```

```json
{ "r": [[1, 2], [2, 3]] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `size` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
