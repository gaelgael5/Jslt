<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `sum`

*[Français](sum.md) · English*

Sum of the numbers in an array (0 for an empty array or null)

```
sum(token)
```

**Example**

```jslt
{ "r": sum($.n) }
```

```json
{ "n": [1, 2, 3] }
```

```json
{ "r": 6 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
