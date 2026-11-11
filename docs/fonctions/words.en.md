<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `words`

*[Français](words.md) · English*

Splits a text into words on whitespace (empty ones are dropped)

```
words(token)
```

**Example**

```jslt
{ "r": words($.t) }
```

```json
{ "t": "  le   petit chat " }
```

```json
{ "r": ["le", "petit", "chat"] }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
