<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `find`

*[Français](find.md) · English*

First element of an array for which the predicate is true, otherwise null

```
find(source, predicate)
```

**Example**

```jslt
{ "trouve": find($.l, $ > 2), "aucun": find($.l, $ > 9) }
```

```json
{ "l": [1, 2, 3, 4] }
```

```json
{ "trouve": 3, "aucun": null }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `predicate` | optional | **unevaluated** expression, computed by the function |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
