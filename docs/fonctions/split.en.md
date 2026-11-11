<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `split`

*[Français](split.md) · English*

Cuts a text into an array on the first character of charset

```
split(token, charset)
```

**Example**

```jslt
{ "r": split($.t, ";") }
```

```json
{ "t": "a;b;c" }
```

```json
{ "r": ["a", "b", "c"] }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `charset` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
