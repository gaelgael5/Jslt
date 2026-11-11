<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `groupby`

*[Français](groupby.md) · English*

Groups an array into an object { key: elements }, key computed per element; nested adds one level per key of an array of keys

```
groupby(source, key, nested)
```

**Examples**

```jslt
{ "plat": groupby($.l, $.ville) }
```

```json
{ "l": [{ "id": 1, "ville": "Lyon" }, { "id": 2, "ville": "Brest" }] }
```

```json
{ "plat": { "Lyon": [{ "id": 1, "ville": "Lyon" }], "Brest": [{ "id": 2, "ville": "Brest" }] } }
```

```jslt
{ "imbrique": groupby($.l, [$.pays, $.ville], true) }
```

```json
{ "l": [{ "id": 1, "pays": "FR", "ville": "Lyon" }] }
```

```json
{ "imbrique": { "FR": { "Lyon": [{ "id": 1, "pays": "FR", "ville": "Lyon" }] } } }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `key` | optional | **unevaluated** expression, computed by the function |
| `nested` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
