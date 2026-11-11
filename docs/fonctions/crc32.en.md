<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `crc32`

*[Français](crc32.md) · English*

CRC32 checksum of a value (unsigned integer)

```
crc32(token)
```

**Example**

```jslt
{ "r": crc32($.t) }
```

```json
{ "t": "abc" }
```

```json
{ "r": 891568578 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Encoding, digests and escaping](../encodage.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
