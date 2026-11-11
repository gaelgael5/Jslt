<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `stddev`

*[Français](stddev.md) · English*

Standard deviation of the numbers in an array: of population by default, of sample when sample is true

```
stddev(token, sample)
```

**Example**

```jslt
{ "population": stddev($.n), "echantillon": round(stddev($.n, true), 3) }
```

```json
{ "n": [2, 4, 4, 4, 5, 5, 7, 9] }
```

```json
{ "population": 2.0, "echantillon": 2.138 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `sample` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
