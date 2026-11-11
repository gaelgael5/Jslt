<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `roundhalfup`

*[Français](roundhalfup.md) · English*

Commercial rounding: halves go away from zero (0.125 -> 0.13), to the integer or to digits decimals

```
roundhalfup(token, digits)
```

**Example**

*`round($.n, 2)` would give `0.12`: it rounds the half to the **even** digit.*

```jslt
{ "commercial": roundhalfup($.n, 2), "bancaire": round($.n, 2) }
```

```json
{ "n": 0.125 }
```

```json
{ "commercial": 0.13, "bancaire": 0.12 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `digits` | optional | number of decimals; absent, rounds to the integer; negative, to tens (`-2` = to the hundred) |

**Good to know**

- **Commercial** rounding, where `round` is banker's: `round(0.125, 2)` gives `0.12`. Halves go **away from zero**, so `-0.5` gives `-1` — a credit note rounds like the invoice it cancels.
- The number is read as it is **written**: `2.675` is stored as `2.67499999…`, and a rounding run on that value would give `2.67`.

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
