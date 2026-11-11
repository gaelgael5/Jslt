<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `shorten`

*[Français](shorten.md) · English*

Shortens a text to length characters at most, suffix included (… by default)

```
shorten(token, length, suffix)
```

**Example**

```jslt
{ "r": shorten($.t, 12) }
```

```json
{ "t": "Facture annuelle 2026" }
```

```json
{ "r": "Facture…" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `length` | optional |  |
| `suffix` | optional |  |

**Good to know**

- The length **includes the suffix** (`…` by default), and the cut backs up to the last space: a word is not cut in half.

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
