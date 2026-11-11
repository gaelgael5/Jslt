<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `selectany`

*[Français](selectany.md) · English*

True when the JSONPath path selects at least one value in the source

```
selectany(source, path)
```

**Example**

```jslt
{ "r": selectany($.d, $.client.nom) }
```

```json
{ "d": { "client": { "nom": "Ana" } } }
```

```json
{ "r": true }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `path` | optional | **unevaluated** JSONPath path |

**Good to know**

- Counts the **nodes** selected, not their truth: a `0` or `""` value found returns `true`.

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
