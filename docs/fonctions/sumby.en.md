<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `sumby`

*[Français](sumby.md) · English*

Sum per computed key, as an object { key: sum } (the value defaults to the element)

```
sumby(source, key, value)
```

**Example**

```jslt
{ "r": sumby($.l, $.ville, $.m) }
```

```json
{ "l": [{ "ville": "Lyon", "m": 10 }, { "ville": "Lyon", "m": 5 }, { "ville": "Brest", "m": 7 }] }
```

```json
{ "r": { "Lyon": 15, "Brest": 7 } }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional | the array to aggregate |
| `key` | optional | the group key expression, evaluated per element · **unevaluated** expression, computed by the function |
| `value` | optional | the expression of the value to sum; omitted, it is the element · **unevaluated** expression, computed by the function |

**Good to know**

- A non-numeric value **raises**, as for `sum`: a total that skips the intruders is plausible and wrong.

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
