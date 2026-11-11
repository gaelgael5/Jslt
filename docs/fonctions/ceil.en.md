<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `ceil`

*[Français](ceil.md) · English*

Rounds up, to the integer (2.1 -> 3.0) or to digits decimals

```
ceil(token, digits)
```

**Example**

```jslt
{ "entier": ceil($.n), "deux_decimales": ceil($.n, 2) }
```

```json
{ "n": 2.341 }
```

```json
{ "entier": 3.0, "deux_decimales": 2.35 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `digits` | optional |  |

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
