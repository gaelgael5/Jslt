<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `some`

*[Français](some.md) · English*

True when the predicate holds for at least one element (false for an empty array)

```
some(source, predicate)
```

**Example**

*`any` says "non-empty array"; `some` tests a predicate.*

```jslt
{ "some": some($.l, $ > 3), "any": any($.l) }
```

```json
{ "l": [1, 2] }
```

```json
{ "some": false, "any": true }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `predicate` | optional | **unevaluated** expression, computed by the function |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
