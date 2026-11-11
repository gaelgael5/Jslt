<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `minby`

*[Français](minby.md) · English*

Element of an array whose computed key is the smallest (null when empty)

```
minby(source, key)
```

**Example**

*Returns the **element**, where `min` returns the extreme value without saying who carries it.*

```jslt
{ "r": map([minby($.l, $.prix)], $.ref) }
```

```json
{ "l": [{ "ref": "A", "prix": 30 }, { "ref": "B", "prix": 10 }] }
```

```json
{ "r": ["B"] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `key` | optional | **unevaluated** expression, computed by the function |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
