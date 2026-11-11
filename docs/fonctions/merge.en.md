<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `merge`

*[Français](merge.md) · English*

Merges two objects, the right one winning the shared keys (deep for sub-objects, arrays to concatenate arrays)

```
merge(left, right, deep, arrays)
```

**Example**

```jslt
{ "r": merge($.a, $.b) }
```

```json
{ "a": { "x": 1, "y": 2 }, "b": { "y": 9 } }
```

```json
{ "r": { "x": 1, "y": 9 } }
```

| Parameter | Expected | Note |
|---|---|---|
| `left` | optional |  |
| `right` | optional |  |
| `deep` | optional |  |
| `arrays` | optional |  |

**Chapter**: [Objects and deep structures](../objets.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
