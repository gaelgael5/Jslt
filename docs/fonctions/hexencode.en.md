<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `hexencode`

*[Français](hexencode.md) · English*

Writes the UTF-8 bytes of a value in hexadecimal

```
hexencode(token)
```

**Example**

```jslt
{ "r": hexencode($.t) }
```

```json
{ "t": "abc" }
```

```json
{ "r": "616263" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Encoding, digests and escaping](../encodage.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
