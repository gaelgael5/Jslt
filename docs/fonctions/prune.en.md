<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `prune`

*[Français](prune.md) · English*

Recursively removes the nulls of a structure, and the empties with the empty option

```
prune(token, options)
```

**Example**

```jslt
{ "nulls": prune($.o), "vides_aussi": prune($.o, "empty") }
```

```json
{ "o": { "a": 1, "b": null, "c": "" } }
```

```json
{ "nulls": { "a": 1, "c": "" }, "vides_aussi": { "a": 1 } }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `options` | optional |  |

**Good to know**

- By default only `null`s go: `0`, `false` and `""` are **values**, and dropping an "amount: 0" would lose information.
- The `"empty"` option also removes empty strings, arrays and objects — but keeps `0` and `false`.

**Chapter**: [Objects and deep structures](../objets.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
