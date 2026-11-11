<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `schema`

*[Français](schema.md) · English*

JSON Schema (draft-04) inferred from a sample JSON fragment

```
schema(fragment)
```

**Example**

```jslt
{ "r": schema($.o) }
```

```json
{ "o": { "nom": "Ana" } }
```

```json
{ "r": { "$schema": "http://json-schema.org/draft-04/schema#", "type": "object", "properties": { "nom": { "type": "string" } } } }
```

| Parameter | Expected | Note |
|---|---|---|
| `fragment` | optional |  |

**Chapter**: [Types, error fallback and validation](../types.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
