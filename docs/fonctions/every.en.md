<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `every`

*[Français](every.md) · English*

True when the predicate holds for every element (true for an empty array)

```
every(source, predicate)
```

**Example**

*True on an **empty** array: there is no counter-example.*

```jslt
{ "tous": every($.l, $ > 0), "vide": every($.v, $ > 0) }
```

```json
{ "l": [1, 2], "v": [] }
```

```json
{ "tous": true, "vide": true }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `predicate` | optional | **unevaluated** expression, computed by the function |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
