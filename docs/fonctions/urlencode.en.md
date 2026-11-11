<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `urlencode`

*[Français](urlencode.md) · English*

Encodes a value for a URL (path mode to keep the slashes)

```
urlencode(token, mode)
```

**Example**

```jslt
{ "r": urlencode($.t) }
```

```json
{ "t": "café noir" }
```

```json
{ "r": "caf%C3%A9%20noir" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `mode` | optional |  |

**Chapter**: [Encoding, digests and escaping](../encodage.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
