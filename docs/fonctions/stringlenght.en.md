<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `stringlenght`

*[Français](stringlenght.md) · English*

Number of characters of a text (0 for null or a non-string) — original spelling kept

```
stringlenght(token)
```

**Example**

```jslt
{ "r": stringlenght($.t) }
```

```json
{ "t": "bonjour" }
```

```json
{ "r": 7 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
