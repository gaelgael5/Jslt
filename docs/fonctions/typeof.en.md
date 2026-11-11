<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `typeof`

*[Français](typeof.md) · English*

JSON type of a value: null, boolean, number, string, array or object

```
typeof(token)
```

**Example**

```jslt
{ "texte": typeof($.t), "tableau": typeof($.l), "absent": typeof($.z) }
```

```json
{ "t": "a", "l": [] }
```

```json
{ "texte": "string", "tableau": "array", "absent": "null" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Types, error fallback and validation](../types.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
