<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `unflatten`

*[Français](unflatten.md) · English*

Rebuilds a nested object from dotted keys (arrays true for the indices)

```
unflatten(token, separator, arrays)
```

**Example**

```jslt
{ "r": unflatten($.o) }
```

```json
{ "o": { "client.nom": "Ana" } }
```

```json
{ "r": { "client": { "nom": "Ana" } } }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `separator` | optional |  |
| `arrays` | optional |  |

**Good to know**

- Numeric segments only become **arrays** when `arrays` is `true`: a key "2026" is a year's name in half of real documents, and turning it into an index would create an array with two thousand holes.
- A path conflict (`a` being 1 and `a.b` being 2) **raises**.

**Chapter**: [Objects and deep structures](../objets.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
