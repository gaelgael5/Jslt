<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `limit`

*[Français](limit.md) · English*

The first max_items elements of an array

```
limit(source, max_items)
```

**Example**

```jslt
{ "r": limit($.l, 2) }
```

```json
{ "l": [1, 2, 3, 4] }
```

```json
{ "r": [1, 2] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `max_items` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
