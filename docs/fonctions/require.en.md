<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `require`

*[Français](require.md) · English*

Returns the value when it is present, otherwise raises with the given message

```
require(value, message)
```

**Example**

```jslt
{ "r": require($.n, "le montant est obligatoire") }
```

```json
{ "n": 0 }
```

```json
{ "r": 0 }
```

| Parameter | Expected | Note |
|---|---|---|
| `value` | optional |  |
| `message` | optional |  |

**Good to know**

- Only refuses **absence**: `0`, `false` and `""` are values and pass. For a condition, use `requirethat`.
- The error is a `JsltError` carrying the message: it can therefore be caught by `trydefault`.

**Chapter**: [Quality: refuse, observe, validate](../qualite.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
