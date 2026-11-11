<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `floor`

*[Français](floor.md) · English*

Rounds down, to the integer (2.7 -> 2.0) or to digits decimals

```
floor(token, digits)
```

**Example**

```jslt
{ "entier": floor($.n), "deux_decimales": floor($.n, 2) }
```

```json
{ "n": 2.349 }
```

```json
{ "entier": 2.0, "deux_decimales": 2.34 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `digits` | optional |  |

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
