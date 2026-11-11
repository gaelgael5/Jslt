<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `pick`

*[Français](pick.md) · English*

Sub-object limited to the requested keys (one key or an array of keys)

```
pick(token, keys)
```

**Example**

```jslt
{ "r": pick($.o, ["nom", "ville"]) }
```

```json
{ "o": { "nom": "Ana", "ville": "Lyon", "secret": "x" } }
```

```json
{ "r": { "nom": "Ana", "ville": "Lyon" } }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `keys` | optional |  |

**Good to know**

- Accepts a single key (`"name"`) or an array of keys. A missing key is ignored: it does not appear as `null` in the result.

**Chapter**: [Objects and deep structures](../objets.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
