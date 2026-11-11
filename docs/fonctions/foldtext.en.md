<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `foldtext`

*[Français](foldtext.md) · English*

Comparison key for a text: lowercase without accents by default, or case / accents only

```
foldtext(token, options)
```

**Example**

```jslt
{ "r": foldtext($.t) }
```

```json
{ "t": "Évêché" }
```

```json
{ "r": "eveche" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `options` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
