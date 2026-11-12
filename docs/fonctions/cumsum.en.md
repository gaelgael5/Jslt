<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `cumsum`

*[Français](cumsum.md) · English*

Running totals of an array of numbers ([1,2,3] -> [1,3,6])

```
cumsum(source)
```

**Example**

```jslt
{ "r": cumsum($.l) }
```

```json
{ "l": [1, 2, 3, 4] }
```

```json
{ "r": [1, 3, 6, 10] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
