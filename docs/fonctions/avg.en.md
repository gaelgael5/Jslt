<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `avg`

*[Français](avg.md) · English*

Mean of the numbers in an array (null for an empty array)

```
avg(token)
```

**Example**

```jslt
{ "r": avg($.n) }
```

```json
{ "n": [1, 2, 6] }
```

```json
{ "r": 3.0 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
