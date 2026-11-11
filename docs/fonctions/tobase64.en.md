<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `tobase64`

*[Français](tobase64.md) · English*

Encodes a value in Base64 (UTF-8 text; object or array serialised as JSON)

```
tobase64(token)
```

**Example**

```jslt
{ "r": tobase64($.t) }
```

```json
{ "t": "bonjour" }
```

```json
{ "r": "Ym9uam91cg==" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Encoding, digests and escaping](../encodage.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
