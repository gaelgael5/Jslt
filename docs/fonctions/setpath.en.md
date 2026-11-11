<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `setpath`

*[Français](setpath.md) · English*

Copy of the object with a value placed at the end of a dotted path (levels created as needed)

```
setpath(token, path, value, separator)
```

**Example**

```jslt
{ "r": setpath($.o, "client.ville", "Lyon") }
```

```json
{ "o": { "client": { "nom": "Ana" } } }
```

```json
{ "r": { "client": { "nom": "Ana", "ville": "Lyon" } } }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `path` | optional |  |
| `value` | optional |  |
| `separator` | optional |  |

**Good to know**

- Returns a **copy**: the source is not modified. Missing levels are created, and the separator is adjustable (4th argument).

**Chapter**: [Objects and deep structures](../objets.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
