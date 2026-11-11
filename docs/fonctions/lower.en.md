<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `lower`

*[Français](lower.md) · English*

Text in lower case (null stays null, a non-string gives false)

```
lower(token)
```

**Example**

```jslt
{ "r": lower($.t) }
```

```json
{ "t": "ACME SA" }
```

```json
{ "r": "acme sa" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
