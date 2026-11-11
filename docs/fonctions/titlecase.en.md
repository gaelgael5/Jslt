<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `titlecase`

*[Français](titlecase.md) · English*

Upper-cases the first letter of every word, leaving the rest alone

```
titlecase(token)
```

**Example**

```jslt
{ "r": titlecase($.t) }
```

```json
{ "t": "ana de la tour" }
```

```json
{ "r": "Ana De La Tour" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
