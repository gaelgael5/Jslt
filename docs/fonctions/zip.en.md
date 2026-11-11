<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `zip`

*[Français](zip.md) · English*

Pairs two arrays element by element, stopping at the shorter one

```
zip(left, right)
```

**Example**

```jslt
{ "r": zip($.a, $.b) }
```

```json
{ "a": [1, 2], "b": ["x", "y"] }
```

```json
{ "r": [[1, "x"], [2, "y"]] }
```

| Parameter | Expected | Note |
|---|---|---|
| `left` | optional |  |
| `right` | optional |  |

**Good to know**

- Stops at the shorter one rather than padding with `null`: an invented pair would be indistinguishable from a genuine null value.

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
