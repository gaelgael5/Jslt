<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `avgby`

*[Français](avgby.md) · English*

Mean per computed key, as an object { key: mean } (the value defaults to the element)

```
avgby(source, key, value)
```

**Example**

```jslt
{ "r": avgby($.l, $.ville, $.m) }
```

```json
{ "l": [{ "ville": "Lyon", "m": 10 }, { "ville": "Lyon", "m": 20 }, { "ville": "Brest", "m": 7 }] }
```

```json
{ "r": { "Lyon": 15.0, "Brest": 7.0 } }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional | the array to aggregate |
| `key` | optional | the group key expression, evaluated per element · **unevaluated** expression, computed by the function |
| `value` | optional | the expression of the value to average; omitted, it is the element · **unevaluated** expression, computed by the function |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
