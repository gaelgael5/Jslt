<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `sign`

*[Français](sign.md) · English*

Sign of a number: -1, 0 or 1

```
sign(token)
```

**Example**

```jslt
{ "negatif": sign($.a), "zero": sign($.b), "positif": sign($.c) }
```

```json
{ "a": -4, "b": 0, "c": 7 }
```

```json
{ "negatif": -1, "zero": 0, "positif": 1 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
