<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `any`

*[Français](any.md) · English*

True when the source is a non-empty array (with a predicate, that is some)

```
any(source)
```

**Example**

```jslt
{ "pleine": any($.l), "vide": any($.v) }
```

```json
{ "l": [1], "v": [] }
```

```json
{ "pleine": true, "vide": false }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
