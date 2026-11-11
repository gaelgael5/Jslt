<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `regexreplace`

*[Français](regexreplace.md) · English*

Replaces the matches of a regex pattern ($1, ${name}, $& for the groups)

```
regexreplace(token, pattern, replacement)
```

**Example**

```jslt
{ "r": regexreplace($.t, "(\\d{4})-(\\d{2})", "$2/$1") }
```

```json
{ "t": "2026-11" }
```

```json
{ "r": "11/2026" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `pattern` | optional |  |
| `replacement` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
