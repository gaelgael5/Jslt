<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `clamp`

*[Français](clamp.md) · English*

Brings a number back into the [lower, upper] range

```
clamp(token, lower, upper)
```

**Example**

```jslt
{ "r": clamp($.n, 0, 100) }
```

```json
{ "n": 142 }
```

```json
{ "r": 100 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `lower` | optional |  |
| `upper` | optional |  |

**Good to know**

- A value that is not a number gives `null` rather than being brought back to a bound.

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
