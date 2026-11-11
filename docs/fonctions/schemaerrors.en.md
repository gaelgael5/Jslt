<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `schemaerrors`

*[Français](schemaerrors.md) · English*

List of the validation errors of a document against a JSON Schema (empty when it conforms)

```
schemaerrors(fragment, schema_document)
```

**Example**

```jslt
{ "r": schemaerrors($.o, $.s) }
```

```json
{ "o": { "age": "vieux" }, "s": { "type": "object", "properties": { "age": { "type": "integer" } } } }
```

```json
{ "r": ["$.age : attendu un entier, reçu une chaîne"] }
```

| Parameter | Expected | Note |
|---|---|---|
| `fragment` | optional |  |
| `schema_document` | optional |  |

**Chapter**: [Types, error fallback and validation](../types.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
