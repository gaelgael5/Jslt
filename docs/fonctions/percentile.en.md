<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `percentile`

*[Français](percentile.md) · English*

Percentile p (0 to 100) of the numbers in an array, by linear interpolation

```
percentile(token, p)
```

**Example**

```jslt
{ "p90": percentile($.n, 90) }
```

```json
{ "n": [1, 2, 3, 4, 5] }
```

```json
{ "p90": 4.6 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `p` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
