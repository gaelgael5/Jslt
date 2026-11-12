<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `chars`

*[Français](chars.md) · English*

Splits a text into an array of characters (by grapheme)

```
chars(token)
```

**Example**

*By **grapheme**: an "e" followed by a combining accent stays one character.*

```jslt
{ "r": chars($.t) }
```

```json
{ "t": "été" }
```

```json
{ "r": ["é", "t", "é"] }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
