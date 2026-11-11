<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `trim`

*[Français](trim.md) · English*

Removes the spaces at both ends, or the characters of txt when it is given

```
trim(token, txt)
```

**Example**

```jslt
{ "espaces": trim($.a), "caracteres": trim($.b, "*") }
```

```json
{ "a": "  ok  ", "b": "**ok**" }
```

```json
{ "espaces": "ok", "caracteres": "ok" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `txt` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
