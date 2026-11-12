<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `map`

*[Français](map.md) · English*

Applies an expression to each element of an array and returns the results

```
map(source, expression)
```

**Example**

*What the loop already does — but usable **as an argument**.*

```jslt
{ "noms": map($.l, $.n), "total": sum(map($.l, $.age)) }
```

```json
{ "l": [{ "n": "Ana", "age": 30 }, { "n": "Bo", "age": 25 }] }
```

```json
{ "noms": ["Ana", "Bo"], "total": 55 }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `expression` | optional | **unevaluated** expression, computed by the function |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
