<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `createindex`

*[Français](createindex.md) · English*

Builds an index {key: element} from a source, a splitting path and a key path

```
createindex(source, object_path, key)
```

**Example**

```jslt
{ "i:": createindex($.p, "", "$.nom"), "ana": index(i:, "Ana") }
```

```json
{ "p": [{ "nom": "Ana", "ville": "Lyon" }] }
```

```json
{ "ana": { "nom": "Ana", "ville": "Lyon" } }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `object_path` | optional |  |
| `key` | optional |  |

**Good to know**

- Goes into a variable (`"i:": createindex(…)`) that `index(i:, key)` then queries. The 2nd argument is the **splitting** path (empty = the whole source).

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
