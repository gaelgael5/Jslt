<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `tohex`

*[Français](tohex.md) · English*

Writes an integer in lower-case hexadecimal, padded to width digits

```
tohex(token, width)
```

**Example**

```jslt
{ "r": tohex($.n), "sur_quatre": tohex($.n, 4) }
```

```json
{ "n": 255 }
```

```json
{ "r": "ff", "sur_quatre": "00ff" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `width` | optional |  |

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
