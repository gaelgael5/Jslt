<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `traces`

*[Français](traces.md) · English*

Journal of the values observed by trace() in this run

```
traces()
```

**Example**

```jslt
{ "r": trace($.n, "montant"), "journal": traces() }
```

```json
{ "n": 42 }
```

```json
{ "r": 42, "journal": [{ "label": "montant", "value": 42 }] }
```

This function takes no argument.

**Chapter**: [Quality: refuse, observe, validate](../qualite.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
