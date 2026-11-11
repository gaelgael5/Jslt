<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `shiftleft`

*[Français](shiftleft.md) · English*

Shifts the bits of an integer to the left (multiplies by 2^bits)

```
shiftleft(token, bits)
```

**Example**

```jslt
{ "r": shiftleft($.n, 3) }
```

```json
{ "n": 1 }
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
