<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `values`

*[Français](values.md) · English*

Values of an object, in document order (null when it is not an object)

```
values(token)
```

**Example**

```jslt
{ "r": values($.o) }
```

```json
{ "o": { "a": 1, "b": 2 } }
```

```json
{ "r": [1, 2] }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Objects and deep structures](../objets.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
