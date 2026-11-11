<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `md5`

*[Français](md5.md) · English*

MD5 digest of a value, in hexadecimal (identity, not signature)

```
md5(token)
```

**Example**

```jslt
{ "r": md5($.t) }
```

```json
{ "t": "abc" }
```

```json
{ "r": "900150983cd24fb0d6963f7d28e17f72" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Good to know**

- For **identity** only: MD5 is broken for any security use.

**Chapter**: [Encoding, digests and escaping](../encodage.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
