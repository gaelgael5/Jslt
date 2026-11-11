<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `contains`

*[Français](contains.md) · English*

True when the array holds an element equal to the value

```
contains(source, to_match)
```

**Example**

```jslt
{ "r": contains($.l, "b") }
```

```json
{ "l": ["a", "b"] }
```

```json
{ "r": true }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `to_match` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
