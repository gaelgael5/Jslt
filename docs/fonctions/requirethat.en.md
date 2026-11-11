<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `requirethat`

*[Français](requirethat.md) · English*

Checks a condition and raises with the given message when it is not true

```
requirethat(condition, message)
```

**Example**

```jslt
{ "r": trydefault(requirethat($.n > 100, "montant trop faible"), "refusé") }
```

```json
{ "n": 10 }
```

```json
{ "r": "refusé" }
```

| Parameter | Expected | Note |
|---|---|---|
| `condition` | optional |  |
| `message` | optional |  |

**Chapter**: [Quality: refuse, observe, validate](../qualite.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
