<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `findindex`

*[Français](findindex.md) · English*

Position of the first element satisfying the predicate, -1 when there is none

```
findindex(source, predicate)
```

**Example**

```jslt
{ "position": findindex($.l, $ > 2), "aucune": findindex($.l, $ > 9) }
```

```json
{ "l": [1, 2, 3, 4] }
```

```json
{ "position": 2, "aucune": -1 }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `predicate` | optional | **unevaluated** expression, computed by the function |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
