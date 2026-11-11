<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `deaccent`

*[Français](deaccent.md) · English*

Removes diacritics (accents, cedillas) without touching the case

```
deaccent(token)
```

**Example**

```jslt
{ "r": deaccent($.t) }
```

```json
{ "t": "Évêché" }
```

```json
{ "r": "Eveche" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
