<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `omit`

*[Français](omit.md) · English*

Object without the requested keys (one key or an array of keys)

```
omit(token, keys)
```

**Example**

```jslt
{ "r": omit($.o, ["secret"]) }
```

```json
{ "o": { "nom": "Ana", "secret": "x" } }
```

```json
{ "r": { "nom": "Ana" } }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `keys` | optional |  |

**Chapter**: [Objects and deep structures](../objets.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
