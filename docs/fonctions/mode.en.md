<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `mode`

*[Français](mode.md) · English*

Most frequent value of an array (the first one seen in case of a tie)

```
mode(token)
```

**Example**

```jslt
{ "r": mode($.l) }
```

```json
{ "l": ["a", "b", "a"] }
```

```json
{ "r": "a" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Good to know**

- Accepts **any** values, not only numbers: the most frequent label is meaningful. On a tie, the **first seen** wins.

**Chapter**: [Data and collections](../collections.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
