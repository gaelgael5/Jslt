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

**Good to know**

- Bases from 2 to 36 (digits then lower-case letters). `width` pads with leading zeros; the sign is written **in front of** the digits, a JSON integer having no fixed width.

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
