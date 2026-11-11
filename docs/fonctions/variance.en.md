<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `variance`

*[Français](variance.md) · English*

Variance of the numbers in an array: of population by default, of sample when sample is true

```
variance(token, sample)
```

**Example**

```jslt
{ "r": variance($.n) }
```

```json
{ "n": [2, 4, 4, 4, 5, 5, 7, 9] }
```

```json
{ "r": 4.0 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `sample` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
