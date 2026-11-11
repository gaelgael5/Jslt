<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `tobase`

*[Français](tobase.md) · English*

Writes an integer in a base from 2 to 36, padded to width digits

```
tobase(token, base, width)
```

**Example**

```jslt
{ "binaire": tobase($.n, 2), "sur_huit": tobase($.n, 2, 8) }
```

```json
{ "n": 11 }
```

```json
{ "binaire": "1011", "sur_huit": "00001011" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `base` | optional |  |
| `width` | optional |  |

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
