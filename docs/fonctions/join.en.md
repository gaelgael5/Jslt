<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `join`

*[Français](join.md) · English*

Left join between two arrays: attaches to the left objects the right elements sharing the key (joining text is concat)

```
join(source_left, key_left, clean_source, rights)
```

**Example**

```jslt
{ "r": join($.c, $.id, false, [{ "Name": "commandes", "Key": "$.client", "Source": $.o }]) }
```

```json
{ "c": [{ "id": 1, "nom": "Ana" }], "o": [{ "client": 1, "total": 12 }] }
```

```json
{ "r": [{ "id": 1, "nom": "Ana", "commandes": [{ "total": 12 }] }] }
```

| Parameter | Expected | Note |
|---|---|---|
| `source_left` | optional |  |
| `key_left` | optional | **unevaluated** JSONPath path |
| `clean_source` | optional |  |
| `rights` | optional |  |

**Good to know**

- A **left** join: each left object receives, under `Name`, the elements of `Source` whose `Key` is equal (compared as text). The source is not modified.

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
