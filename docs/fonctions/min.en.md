<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `min`

*[Français](min.md) · English*

Smaller of two numbers, or of the given array (decimal for two numbers)

```
min(left, right)
```

**Example**

```jslt
{ "deux": min($.a, $.b), "du_tableau": min($.l) }
```

```json
{ "a": 2, "b": 9, "l": [3, 11, 7] }
```

```json
{ "deux": 2.0, "du_tableau": 3 }
```

| Parameter | Expected | Note |
|---|---|---|
| `left` | optional |  |
| `right` | optional |  |

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
