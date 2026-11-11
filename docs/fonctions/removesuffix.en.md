<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `removesuffix`

*[Français](removesuffix.md) · English*

Removes a whole suffix when present, otherwise returns the text unchanged

```
removesuffix(token, suffix)
```

**Example**

```jslt
{ "present": removesuffix($.t, ".json"), "absent": removesuffix($.t, ".xml") }
```

```json
{ "t": "contrat.json" }
```

```json
{ "present": "contrat", "absent": "contrat.json" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `suffix` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
