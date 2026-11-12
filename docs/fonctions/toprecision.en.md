<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `toprecision`

*[Français](toprecision.md) · English*

Rounds to a number of significant digits (toprecision(1234.5, 3) -> 1230)

```
toprecision(token, digits)
```

**Example**

*Three significant digits, whatever the order of magnitude.*

```jslt
{ "grand": toprecision($.a, 3), "petit": toprecision($.b, 3) }
```

```json
{ "a": 1234.5, "b": 0.00241348 }
```

```json
{ "grand": 1230.0, "petit": 0.00241 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `digits` | optional | number of **significant** digits, at least 1 (not a number of decimals) |

**Good to know**

- **Significant** digits, not decimals: `round($.n, 2)` fixes where the decimal point falls, which makes no sense in a column where `0.00241` sits next to `24100`.
- Fewer than one digit **raises**; `0` is returned as is, since zero has as many significant digits as one likes.

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
