<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `shiftright`

*[Français](shiftright.md) · English*

Shifts the bits of an integer to the right (divides by 2^bits)

```
shiftright(token, bits)
```

**Example**

```jslt
{ "r": shiftright($.n, 3) }
```

```json
{ "n": 64 }
```

```json
{ "r": 8 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `bits` | optional |  |

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
