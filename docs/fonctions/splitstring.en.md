<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `splitstring`

*[Français](splitstring.md) · English*

Cuts a text on a whole separator (several characters), at most limit times

```
splitstring(token, separator, limit)
```

**Example**

```jslt
{ "r": splitstring($.t, " - ") }
```

```json
{ "t": "a - b - c" }
```

```json
{ "r": ["a", "b", "c"] }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `separator` | optional |  |
| `limit` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
