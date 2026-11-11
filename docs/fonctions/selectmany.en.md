<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `selectmany`

*[Français](selectmany.md) · English*

All the values selected by a JSONPath path in the source

```
selectmany(source, path)
```

**Example**

```jslt
{ "r": selectmany($.l, $.*.id) }
```

```json
{ "l": [{ "id": 1 }, { "id": 2 }] }
```

```json
{ "r": [1, 2] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `path` | optional | **unevaluated** JSONPath path |

**Good to know**

- A path argument applied to `source`, like `select`, but it returns **all** the selected values, in document order.

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
