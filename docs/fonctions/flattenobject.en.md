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

**Good to know**

- Arrays are indexed by **position** (`l.0`, `l.1`): this is the bridge to a CSV, which has no depth.

**Chapter**: [Objects and deep structures](../objets.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
