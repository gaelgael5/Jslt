<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `truncate`

*[Français](truncate.md) · English*

Cuts towards zero (-2.7 -> -2.0), to the integer or to digits decimals

```
truncate(token, digits)
```

**Example**

```jslt
{ "vers_zero": truncate($.n), "deux_decimales": truncate($.n, 2) }
```

```json
{ "n": -2.789 }
```

```json
{ "vers_zero": -2.0, "deux_decimales": -2.78 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `digits` | optional |  |

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
