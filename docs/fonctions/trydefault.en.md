<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `trydefault`

*[Français](trydefault.md) · English*

Value of the expression, or that of the fallback when the expression raises an error

```
trydefault(expression, fallback)
```

**Example**

```jslt
{ "r": trydefault($.a / $.b, "division impossible") }
```

```json
{ "a": 1, "b": 0 }
```

```json
{ "r": "division impossible" }
```

| Parameter | Expected | Note |
|---|---|---|
| `expression` | optional | **unevaluated** expression, computed by the function |
| `fallback` | optional | **unevaluated** expression, computed by the function |

**Good to know**

- The fallback is evaluated **only** when the first expression raises: it can therefore be expensive without slowing the nominal case.
- It only catches engine errors (`JsltError`), not a `null` value: for a fallback on absence, use the `??` operator.

**Chapter**: [Types, error fallback and validation](../types.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
