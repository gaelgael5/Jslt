<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `hmacsha256`

*[Français](hmacsha256.md) · English*

HMAC-SHA256 signature of a value with a secret key, in hexadecimal

```
hmacsha256(token, key)
```

**Example**

```jslt
{ "r": hmacsha256($.t, $.cle) }
```

```json
{ "t": "message", "cle": "secret" }
```

```json
{ "r": "8b5f48702995c1598c573db1e21866a9b825d4a794d169d7060a03605796360b" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `key` | optional |  |

**Chapter**: [Encoding, digests and escaping](../encodage.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
