<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `parsejson`

*[Français](parsejson.md) · English*

Reads JSON text and returns the matching value (object, array or scalar)

```
parsejson(token)
```

**Example**

```jslt
{ "r": select(parsejson($.t), $.ville) }
```

```json
{ "t": "{\"ville\": \"Lyon\"}" }
```

```json
{ "r": "Lyon" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Types, error fallback and validation](../types.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
