<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isnull`

*[Français](isnull.md) · English*

True when the value is null or absent

```
isnull(token)
```

**Example**

```jslt
{ "absente": isnull($.z), "vide": isnull($.t) }
```

```json
{ "t": "" }
```

```json
{ "absente": true, "vide": false }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Types, error fallback and validation](../types.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
