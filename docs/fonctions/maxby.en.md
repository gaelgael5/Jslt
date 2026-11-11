<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `maxby`

*[Français](maxby.md) · English*

Element of an array whose computed key is the largest (null when empty)

```
maxby(source, key)
```

**Example**

```jslt
{ "r": map([maxby($.l, $.prix)], $.ref) }
```

```json
{ "l": [{ "ref": "A", "prix": 30 }, { "ref": "B", "prix": 10 }] }
```

```json
{ "r": ["A"] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `key` | optional | **unevaluated** expression, computed by the function |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
