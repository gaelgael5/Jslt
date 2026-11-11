<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `group`

*[Français](group.md) · English*

Groups an array by successive JSONPath paths into nested {Label, Items}

```
group(source, group_paths)
```

**Example**

```jslt
{ "r": group($.p, ["$.ville"]) }
```

```json
{ "p": [{ "nom": "Ana", "ville": "Lyon" }] }
```

```json
{ "r": [{ "Label": "Lyon", "Items": [{ "nom": "Ana", "ville": "Lyon" }] }] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source` | optional |  |
| `group_paths` | optional |  |

**Good to know**

- Returns `{Label, Items}` groups, nested when several paths are given. `groupby` returns an **object**, reducible with `entries`.

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
