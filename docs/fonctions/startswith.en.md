<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `startswith`

*[Français](startswith.md) · English*

True when the text starts with txt

```
startswith(token, txt)
```

**Example**

```jslt
{ "r": startswith($.t, "FR") }
```

```json
{ "t": "FR7630006000011234567890189" }
```

```json
{ "r": true }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `txt` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
