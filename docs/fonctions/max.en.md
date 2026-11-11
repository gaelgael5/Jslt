<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `max`

*[Français](max.md) · English*

Larger of two numbers, or of the given array (decimal for two numbers)

```
max(left, right)
```

**Example**

```jslt
{ "deux": max($.a, $.b), "du_tableau": max($.l) }
```

```json
{ "a": 2, "b": 9, "l": [3, 11, 7] }
```

```json
{ "deux": 9.0, "du_tableau": 11 }
```

| Parameter | Expected | Note |
|---|---|---|
| `left` | optional |  |
| `right` | optional |  |

**Good to know**

- Two forms: two numbers (a **decimal** result) or an array (the **type is preserved**). An array *and* a second argument raises.

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
