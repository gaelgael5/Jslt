<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `renamekeys`

*[Français](renamekeys.md) · English*

Renames the keys of an object according to a { old: new } mapping

```
renamekeys(token, mapping)
```

**Example**

```jslt
{ "r": renamekeys($.o, { "nom": "name" }) }
```

```json
{ "o": { "nom": "Ana", "ville": "Lyon" } }
```

```json
{ "r": { "name": "Ana", "ville": "Lyon" } }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `mapping` | optional |  |

**Good to know**

- A key not mentioned in the mapping is **kept as is**. On a collision the last write wins: raising would break a migration in progress.

**Chapter**: [Objects and deep structures](../objets.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
