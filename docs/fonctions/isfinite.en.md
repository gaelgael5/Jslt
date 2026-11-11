<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isfinite`

*[Français](isfinite.md) · English*

True when the value is a finite number (neither infinite nor NaN)

```
isfinite(token)
```

**Example**

```jslt
{ "nombre": isfinite($.n), "texte": isfinite($.t) }
```

```json
{ "n": 3, "t": "3" }
```

```json
{ "nombre": true, "texte": false }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
