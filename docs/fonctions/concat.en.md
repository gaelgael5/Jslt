<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `concat`

*[Français](concat.md) · English*

Joins the elements of an array into text, separated by split_char then delimit_char (this is the string "join"; join itself is the SQL-style join)

```
concat(token, split_char, delimit_char)
```

**Example**

```jslt
{ "colle": concat($.l), "joint": concat($.l, "-") }
```

```json
{ "l": ["a", "b", "c"] }
```

```json
{ "colle": "abc", "joint": "a-b-c" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `split_char` | optional |  |
| `delimit_char` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
