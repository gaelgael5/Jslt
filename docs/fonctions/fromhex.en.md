<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `fromhex`

*[Français](fromhex.md) · English*

Reads an integer written in hexadecimal (with or without the 0x prefix)

```
fromhex(token)
```

**Example**

```jslt
{ "r": fromhex($.t) }
```

```json
{ "t": "0xff" }
```

```json
{ "r": 255 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
