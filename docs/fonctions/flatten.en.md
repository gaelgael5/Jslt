<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `flatten`

*[Français](flatten.md) · English*

Flattens an array of arrays, all the way down by default or over depth levels

```
flatten(source, depth)
```

**Example**

```jslt
{ "a_fond": flatten($.l), "un_niveau": flatten($.l, 1) }
```

```json
{ "l": [1, [2, [3]]] }
```

```json
{ "a_fond": [1, 2, 3], "un_niveau": [1, 2, [3]] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `depth` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
