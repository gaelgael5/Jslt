<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `get`

*[Français](get.md) · English*

Value of a computed object key or array index (null when absent)

```
get(token, key)
```

**Example**

*The key comes from the **data**: a path, by contrast, is written in the template.*

```jslt
{ "r": get($.o, $.k), "dernier": get($.l, -1) }
```

```json
{ "o": { "a": 1, "b": 2 }, "k": "b", "l": [7, 8, 9] }
```

```json
{ "r": 2, "dernier": 9 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional | the object or array to read; anything else gives `null` |
| `key` | optional | the key, **computed**: a name for an object, an index for an array (negative from the end) |

**Good to know**

- Missing key, out-of-bounds index, source that is neither object nor array: `null`. There is therefore no fallback argument — `get($.o, $.k) ?? 0` says it, and a fallback as an argument would be evaluated even when the key exists.
- To **require** the value: `require(get($.o, $.k), "unknown price")`. To tell a missing key from a key present but null: `has`.

**Chapter**: [Objects and deep structures](../objets.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
