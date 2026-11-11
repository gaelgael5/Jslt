<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `flattenobject`

*[Français](flattenobject.md) · English*

Flattens an object into dotted keys (a.b.c), arrays indexed by their position

```
flattenobject(token, separator)
```

**Example**

```jslt
{ "r": flattenobject($.o) }
```

```json
{ "o": { "client": { "nom": "Ana" } } }
```

```json
{ "r": { "client.nom": "Ana" } }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `separator` | optional |  |

**Chapter**: [Objects and deep structures](../objets.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
