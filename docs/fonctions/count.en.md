<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `count`

*[Français](count.md) · English*

Number of items: elements of an array, keys of an object, characters of a text, 0 for null

```
count(token)
```

**Example**

```jslt
{ "tableau": count($.l), "objet": count($.o), "texte": count($.t) }
```

```json
{ "l": [1, 2], "o": { "a": 1 }, "t": "abc" }
```

```json
{ "tableau": 2, "objet": 1, "texte": 3 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Good to know**

- Counts the elements of an array, the **keys** of an object, the **characters** of a text; a scalar counts as 1 (it is a value) and `null` as 0 (it is an absence).

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
