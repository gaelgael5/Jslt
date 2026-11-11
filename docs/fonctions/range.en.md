<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `range`

*[Français](range.md) · English*

A series of integers: range(end), range(start, end) or range(start, end, step); the end is excluded

```
range(start, end, step)
```

**Examples**

*The **end is excluded**, and a single argument counts from zero.*

```jslt
{ "depuis_zero": range(5), "bornes": range(2, 5), "pas": range(0, 10, 3), "descendant": range(3, 0, -1) }
```

```json
{}
```

```json
{ "depuis_zero": [0, 1, 2, 3, 4], "bornes": [2, 3, 4], "pas": [0, 3, 6, 9], "descendant": [3, 2, 1] }
```

*The only function that **creates** a series: everything else transforms what comes in.*

```jslt
{ "carres": map(range(1, 5), $ * $) }
```

```json
{}
```

```json
{ "carres": [1, 4, 9, 16] }
```

| Parameter | Expected | Note |
|---|---|---|
| `start` | optional |  |
| `end` | optional |  |
| `step` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
