<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isurl`

*[Français](isurl.md) · English*

True when the text has the shape of a URL with its scheme

```
isurl(token)
```

**Example**

```jslt
{ "r": isurl($.t) }
```

```json
{ "t": "https://exemple.fr/a" }
```

```json
{ "r": true }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Quality: refuse, observe, validate](../qualite.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
