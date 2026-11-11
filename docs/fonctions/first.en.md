<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `first`

*[Français](first.md) · English*

First element of an array, or null when it is empty

```
first(source)
```

**Example**

```jslt
{ "r": first($.l) }
```

```json
{ "l": [3, 1] }
```

```json
{ "r": 3 }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
