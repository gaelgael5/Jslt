<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `regexismatch`

*[Français](regexismatch.md) · English*

True when the text holds a match of the regex pattern

```
regexismatch(token, pattern)
```

**Example**

```jslt
{ "r": regexismatch($.t, "^[A-Z]{2}[0-9]+$") }
```

```json
{ "t": "FR123" }
```

```json
{ "r": true }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `pattern` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
