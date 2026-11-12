<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `stringlength`

*[Français](stringlength.md) · English*

Number of characters of a text (0 for null or a non-string)

```
stringlength(token)
```

**Example**

*The same function as `stringlenght`, whose original spelling is a typo.*

```jslt
{ "r": stringlength($.t) }
```

```json
{ "t": "Ana" }
```

```json
{ "r": 3 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Good to know**

- The same function as `stringlenght`, whose original spelling is a typo: both names register the **same** implementation, so they cannot diverge. Removing the old one would break the templates written with it.

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
