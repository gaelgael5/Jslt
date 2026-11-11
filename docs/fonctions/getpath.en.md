<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `getpath`

*[Français](getpath.md) · English*

Value at the end of a computed dotted path (null when a step is missing)

```
getpath(token, path, separator)
```

**Example**

```jslt
{ "r": getpath($.o, $.champ) }
```

```json
{ "o": { "client": { "ville": "Lyon" } }, "champ": "client.ville" }
```

```json
{ "r": "Lyon" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional | the starting object or array; anything else gives `null` |
| `path` | optional | the dotted path, **computable** (`"client.ville"`, `"lignes.0.ref"`); same steps as `setpath` |
| `separator` | optional | step separator, `.` by default; empty, it raises |

**Good to know**

- The reciprocal of `setpath`, which had none: the steps read the same way, array indices included (`"lignes.0.ref"`).
- A missing step — or a scalar met along the way — gives `null` without raising: that is a path's semantics, and `??` provides the fallback.

**Chapter**: [Objects and deep structures](../objets.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
