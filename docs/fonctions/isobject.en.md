<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isobject`

*[Français](isobject.md) · English*

True when the value is a JSON object

```
isobject(token)
```

**Example**

```jslt
{ "objet": isobject($.o), "tableau": isobject($.l) }
```

```json
{ "o": {}, "l": [] }
```

```json
{ "objet": true, "tableau": false }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Types, error fallback and validation](../types.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
