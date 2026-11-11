<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isnotnull`

*[Français](isnotnull.md) · English*

True when the value is neither null nor absent

```
isnotnull(token)
```

**Example**

```jslt
{ "presente": isnotnull($.a), "absente": isnotnull($.z) }
```

```json
{ "a": 0 }
```

```json
{ "presente": true, "absente": false }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Types, error fallback and validation](../types.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
