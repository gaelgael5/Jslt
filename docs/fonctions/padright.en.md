<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `padright`

*[Français](padright.md) · English*

Pads the text on the right up to length with the 1st character of charset (space by default)

```
padright(token, length, charset)
```

**Example**

```jslt
{ "r": padright($.t, 6, ".") }
```

```json
{ "t": "42" }
```

```json
{ "r": "42...." }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `length` | optional |  |
| `charset` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
