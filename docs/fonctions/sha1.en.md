<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `sha1`

*[Français](sha1.md) · English*

SHA-1 digest of a value, in hexadecimal (identity, not signature)

```
sha1(token)
```

**Example**

```jslt
{ "r": sha1($.t) }
```

```json
{ "t": "abc" }
```

```json
{ "r": "a9993e364706816aba3e25717850c26c9cd0d89d" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Encoding, digests and escaping](../encodage.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
