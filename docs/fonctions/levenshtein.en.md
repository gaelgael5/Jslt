<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `levenshtein`

*[Français](levenshtein.md) · English*

Number of characters to insert, delete or replace to go from one text to the other

```
levenshtein(left, right)
```

**Example**

```jslt
{ "r": levenshtein($.a, $.b) }
```

```json
{ "a": "chat", "b": "chats" }
```

```json
{ "r": 1 }
```

| Parameter | Expected | Note |
|---|---|---|
| `left` | optional |  |
| `right` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
