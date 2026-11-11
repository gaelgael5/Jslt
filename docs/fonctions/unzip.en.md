<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `unzip`

*[Français](unzip.md) · English*

Converse of zip: from an array of rows, returns one array per position

```
unzip(source)
```

**Example**

```jslt
{ "r": unzip($.l) }
```

```json
{ "l": [[1, "a"], [2, "b"]] }
```

```json
{ "r": [[1, 2], ["a", "b"]] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
