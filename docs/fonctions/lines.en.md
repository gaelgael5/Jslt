<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `lines`

*[Français](lines.md) · English*

Splits a text into lines (\n, \r\n or \r), empty lines included

```
lines(token)
```

**Example**

*All three line endings, and **empty** lines are kept.*

```jslt
{ "r": lines($.t) }
```

```json
{ "t": "a\nb\n\nc" }
```

```json
{ "r": ["a", "b", "", "c"] }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
