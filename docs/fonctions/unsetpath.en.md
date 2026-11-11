<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `unsetpath`

*[Français](unsetpath.md) · English*

Copy of the object without the dotted path (no error when it is absent)

```
unsetpath(token, path, separator)
```

**Example**

```jslt
{ "r": unsetpath($.o, "client.secret") }
```

```json
{ "o": { "client": { "nom": "Ana", "secret": "x" } } }
```

```json
{ "r": { "client": { "nom": "Ana" } } }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `path` | optional |  |
| `separator` | optional |  |

**Good to know**

- Returns a copy; a missing path is **not** an error.

**Chapter**: [Objects and deep structures](../objets.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
