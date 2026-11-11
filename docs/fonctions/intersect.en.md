<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `intersect`

*[Français](intersect.md) · English*

Elements of the left array also present on the right, deduplicated

```
intersect(left, right)
```

**Example**

```jslt
{ "r": intersect($.a, $.b) }
```

```json
{ "a": [1, 2, 3], "b": [3, 1] }
```

```json
{ "r": [1, 3] }
```

| Parameter | Expected | Note |
|---|---|---|
| `left` | optional |  |
| `right` | optional |  |

**Good to know**

- **Structural** equality (not `==`, where `"2" == 2`), left order preserved, duplicates removed.

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
