<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `reduce`

*[Français](reduce.md) · English*

Folds an array into a single value; the expression sees { acc, value, index } and returns the new accumulator

```
reduce(source, expression, initial)
```

**Examples**

*The expression sees `{acc, value, index}` and returns the new accumulator.*

```jslt
{ "somme": reduce($.l, $.acc + $.value, 0), "colle": reduce($.t, $.acc + $.value, "") }
```

```json
{ "l": [1, 2, 3, 4], "t": ["a", "b", "c"] }
```

```json
{ "somme": 10, "colle": "abc" }
```

*With no initial value, the fold starts from the **first element**.*

```jslt
{ "r": reduce($.l, max($.acc, $.value)) }
```

```json
{ "l": [3, 9, 2] }
```

```json
{ "r": 9.0 }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `expression` | optional | **unevaluated** expression, computed by the function |
| `initial` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
