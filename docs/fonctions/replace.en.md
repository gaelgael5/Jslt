<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `replace`

*[Français](replace.md) · English*

Replaces every occurrence of search with replacement

```
replace(token, search, replacement)
```

**Example**

```jslt
{ "r": replace($.t, "-", "/") }
```

```json
{ "t": "2026-11-11" }
```

```json
{ "r": "2026/11/11" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `search` | optional |  |
| `replacement` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
