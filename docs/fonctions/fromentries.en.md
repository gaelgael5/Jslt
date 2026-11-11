<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `fromentries`

*[Français](fromentries.md) · English*

Rebuilds an object from an array of { key, value } or of [key, value] pairs

```
fromentries(token)
```

**Example**

```jslt
{ "r": fromentries($.l) }
```

```json
{ "l": [{ "key": "a", "value": 1 }] }
```

```json
{ "r": { "a": 1 } }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Objects and deep structures](../objets.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
