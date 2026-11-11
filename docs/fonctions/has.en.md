<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `has`

*[Français](has.md) · English*

True when the object carries that key, even with a null value

```
has(token, key)
```

**Example**

```jslt
{ "presente": has($.o, "a"), "absente": has($.o, "z") }
```

```json
{ "o": { "a": null } }
```

```json
{ "presente": true, "absente": false }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `key` | optional |  |

**Good to know**

- `has` exists because `isnull` does not tell an **absent key** from a key present **with `null`**: both give `true`, and in a feed those are not the same thing.

**Chapter**: [Objects and deep structures](../objets.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
