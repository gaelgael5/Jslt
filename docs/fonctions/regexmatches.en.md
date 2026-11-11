<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `regexmatches`

*[Français](regexmatches.md) · English*

List of the matches of the regex pattern in the text

```
regexmatches(token, pattern)
```

**Example**

```jslt
{ "r": regexmatches($.t, "[0-9]+") }
```

```json
{ "t": "a1 b22 c333" }
```

```json
{ "r": ["1", "22", "333"] }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `pattern` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
