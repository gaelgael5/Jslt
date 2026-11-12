<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `append`

*[Français](append.md) · English*

Copy of the array with a value added at the end

```
append(source, value)
```

**Example**

*Adds **one** value; an array added becomes a nested element.*

```jslt
{ "valeur": append($.l, 3), "tableau": append($.l, [3, 4]), "source": $.l }
```

```json
{ "l": [1, 2] }
```

```json
{ "valeur": [1, 2, 3], "tableau": [1, 2, [3, 4]], "source": [1, 2] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `value` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
