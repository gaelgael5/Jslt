<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `substring`

*[Français](substring.md) · English*

Extracts length characters from start (negative start = from the end, length absent = to the end)

```
substring(token, start, length)
```

**Example**

```jslt
{ "debut": substring($.t, 0, 3), "depuis_la_fin": substring($.t, -2) }
```

```json
{ "t": "bonjour" }
```

```json
{ "debut": "bon", "depuis_la_fin": "ur" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `start` | optional |  |
| `length` | optional |  |

**Good to know**

- Out-of-range bounds do **not raise**: a start beyond the text gives an empty string, an over-long length stops at the end. A template transforms data it does not choose.
- A **negative** length does raise: that is an authoring mistake.

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
