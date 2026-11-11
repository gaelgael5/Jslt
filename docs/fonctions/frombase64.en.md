<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `frombase64`

*[Français](frombase64.md) · English*

Decodes Base64 text into UTF-8 text

```
frombase64(token)
```

**Example**

```jslt
{ "r": frombase64($.t) }
```

```json
{ "t": "Ym9uam91cg==" }
```

```json
{ "r": "bonjour" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Encoding, digests and escaping](../encodage.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
