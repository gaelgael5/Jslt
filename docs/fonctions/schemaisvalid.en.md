<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `schemaisvalid`

*[Français](schemaisvalid.md) · English*

True when the document satisfies the given JSON Schema (supported subset)

```
schemaisvalid(fragment, schema_document)
```

**Example**

```jslt
{ "r": schemaisvalid($.o, $.s) }
```

```json
{ "o": { "age": 42 }, "s": { "type": "object", "properties": { "age": { "type": "integer" } } } }
```

```json
{ "r": true }
```

| Parameter | Expected | Note |
|---|---|---|
| `fragment` | optional |  |
| `schema_document` | optional |  |

**Chapter**: [Types, error fallback and validation](../types.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
