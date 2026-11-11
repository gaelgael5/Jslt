<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `trimstart`

*[Français](trimstart.md) · English*

Removes the leading spaces, or the characters of txt

```
trimstart(token, txt)
```

**Example**

```jslt
{ "r": trimstart($.t) }
```

```json
{ "t": "   ok" }
```

```json
{ "r": "ok" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `txt` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
