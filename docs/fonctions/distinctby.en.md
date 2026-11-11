<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `distinctby`

*[Français](distinctby.md) · English*

Deduplicates an array on a key computed per element, keeping the first

```
distinctby(source, key)
```

**Example**

```jslt
{ "r": distinctby($.l, $.ville) }
```

```json
{ "l": [{ "id": 1, "ville": "Lyon" }, { "id": 2, "ville": "Lyon" }, { "id": 3, "ville": "Brest" }] }
```

```json
{ "r": [{ "id": 1, "ville": "Lyon" }, { "id": 3, "ville": "Brest" }] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `key` | optional | **unevaluated** expression, computed by the function |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
