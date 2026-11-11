<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `round`

*[Français](round.md) · English*

Rounds to the nearest integer, halves to even (2.5 -> 2.0, 3.5 -> 4.0), returned as a decimal (commercial rounding: roundhalfup)

```
round(token, digits)
```

**Example**

```jslt
{ "pair": round($.a), "deux_decimales": round($.b, 2) }
```

```json
{ "a": 2.5, "b": 1.2345 }
```

```json
{ "pair": 2.0, "deux_decimales": 1.23 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `digits` | optional |  |

**Good to know**

- **Banker's** rounding (to the nearest even): `2.5` gives `2` and `3.5` gives `4`. To cut towards zero use `truncate`; upwards, `ceil`.

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
