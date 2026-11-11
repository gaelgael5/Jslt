<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `filter`

*[Français](filter.md) · English*

Keeps the elements of an array for which the predicate is true

```
filter(source, predicate)
```

**Example**

*The expression is arbitrary: a JSONPath filter cannot call a function.*

```jslt
{ "r": filter($.l, stringcontains($.n, "a")) }
```

```json
{ "l": [{ "n": "Ana" }, { "n": "Bo" }] }
```

```json
{ "r": [{ "n": "Ana" }] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `predicate` | optional | **unevaluated** expression, computed by the function |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
