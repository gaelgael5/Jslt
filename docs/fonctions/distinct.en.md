<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `distinct`

*[Français](distinct.md) · English*

Unique values selected by a JSONPath path in an array, in order of appearance

```
distinct(source, path)
```

**Example**

```jslt
{ "r": distinct($.l, $.*) }
```

```json
{ "l": [1, 2, 2, 3] }
```

```json
{ "r": [1, 2, 3] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `path` | optional | **unevaluated** JSONPath path |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
