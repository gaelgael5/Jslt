<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `last`

*[Français](last.md) · English*

Last element of an array, or null when it is empty

```
last(source)
```

**Example**

```jslt
{ "r": last($.l) }
```

```json
{ "l": [3, 1] }
```

```json
{ "r": 1 }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
