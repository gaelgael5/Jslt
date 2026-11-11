<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isnumber`

*[Français](isnumber.md) · English*

True when the value is a number (a boolean is not one)

```
isnumber(token)
```

**Example**

```jslt
{ "nombre": isnumber($.n), "booleen": isnumber($.b) }
```

```json
{ "n": 3, "b": true }
```

```json
{ "nombre": true, "booleen": false }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Types, error fallback and validation](../types.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
