<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `chunk`

*[Français](chunk.md) · English*

Cuts an array into consecutive slices of size elements

```
chunk(source, size)
```

**Example**

```jslt
{ "r": chunk($.l, 2) }
```

```json
{ "l": [1, 2, 3, 4, 5] }
```

```json
{ "r": [[1, 2], [3, 4], [5]] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `size` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
