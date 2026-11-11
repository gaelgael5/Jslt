<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isboolean`

*[Français](isboolean.md) · English*

True when the value is a boolean (true or false)

```
isboolean(token)
```

**Example**

```jslt
{ "r": isboolean($.b), "nombre": isboolean($.n) }
```

```json
{ "b": false, "n": 0 }
```

```json
{ "r": true, "nombre": false }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Types, error fallback and validation](../types.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
