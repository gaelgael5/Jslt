<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `index`

*[Français](index.md) · English*

Element of an index (built by createindex) for a key, or null (for a computed key in any object, that is get)

```
index(index, key)
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
| `index` | optional |  |
| `key` | optional |  |

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
