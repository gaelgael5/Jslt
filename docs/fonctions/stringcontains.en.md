<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `stringcontains`

*[Français](stringcontains.md) · English*

True when the text holds contain_str

```
stringcontains(token, contain_str)
```

**Example**

```jslt
{ "r": stringcontains($.t, "@") }
```

```json
{ "t": "ana@exemple.fr" }
```

```json
{ "r": true }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `contain_str` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
