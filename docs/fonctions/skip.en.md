<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `skip`

*[Français](skip.md) · English*

Drops the first n elements of an array (the complement of limit)

```
skip(source, count)
```

**Example**

```jslt
{ "r": skip($.l, 2) }
```

```json
{ "l": [1, 2, 3, 4] }
```

```json
{ "r": [3, 4] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `count` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
