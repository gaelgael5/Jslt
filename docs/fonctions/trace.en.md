<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `trace`

*[Français](trace.md) · English*

Returns the value unchanged and records it in the journal, readable through traces()

```
trace(value, label)
```

**Example**

```jslt
{ "r": trace($.n, "montant") }
```

```json
{ "n": 42 }
```

```json
{ "r": 42 }
```

| Parameter | Expected | Note |
|---|---|---|
| `value` | optional |  |
| `label` | optional |  |

**Good to know**

- The journal lives on the **execution context**: two concurrent runs never mix, and an integrator reads it afterwards (`context.traces`) without the template having to copy it into its output.

**Chapter**: [Quality: refuse, observe, validate](../qualite.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
