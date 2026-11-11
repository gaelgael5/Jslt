<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `sort`

*[Français](sort.md) · English*

Sorts an array: on the elements, or on a key computed per element, smallest first (descending true, or one direction per key, for the reverse)

```
sort(source, key, descending)
```

**Examples**

```jslt
{ "par_prix": selectmany(sort($.l, $.prix), $.*.id) }
```

```json
{ "l": [{ "id": 1, "prix": 30 }, { "id": 2, "prix": 10 }] }
```

```json
{ "par_prix": [2, 1] }
```

```jslt
{ "ville_puis_prix_decroissant": selectmany(sort($.l, [$.ville, $.prix], [false, true]), $.*.id) }
```

```json
{ "l": [{ "id": 1, "ville": "Lyon", "prix": 10 }, { "id": 2, "ville": "Lyon", "prix": 30 }, { "id": 3, "ville": "Brest", "prix": 5 }] }
```

```json
{ "ville_puis_prix_decroissant": [3, 2, 1] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `key` | optional | **unevaluated** expression, computed by the function |
| `descending` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
