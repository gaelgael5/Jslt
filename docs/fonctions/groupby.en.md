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
| `source` | optional | the array to group |
| `key` | optional | expression evaluated **per element**; an array for a composite key · **unevaluated** expression, computed by the function |
| `nested` | optional | `true` to nest one object level per key |

**Good to know**

- The key is converted to **text**, since a JSON object key is a string: a composite key gives `["FR","Lyon"]` as compact JSON. `nested` saves you from parsing it back.

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
