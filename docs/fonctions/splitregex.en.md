<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `splitregex`

*[Français](splitregex.md) · English*

Cuts a text on the matches of a regex pattern

```
splitregex(token, pattern, limit)
```

**Example**

```jslt
{ "r": splitregex($.t, "\\s*;\\s*") }
```

```json
{ "t": "a ; b;c" }
```

```json
{ "r": ["a", "b", "c"] }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `pattern` | optional |  |
| `limit` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
