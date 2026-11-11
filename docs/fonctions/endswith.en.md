<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `endswith`

*[Français](endswith.md) · English*

True when the text ends with txt

```
endswith(token, txt)
```

**Example**

```jslt
{ "r": endswith($.t, ".json") }
```

```json
{ "t": "contrat.json" }
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
