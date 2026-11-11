<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `today`

*[Français](today.md) · English*

Today's date at midnight in ISO 8601: local, or UTC when utc is true

```
today(utc)
```

**Example**

```jslt
{ "r": datepart(today(), "hour") }
```

```json
{}
```

```json
{ "r": 0 }
```

| Parameter | Expected | Note |
|---|---|---|
| `utc` | optional |  |

**Good to know**

- **Local** midnight, or UTC when `utc` is `true`. Like `now`, it makes a template non-deterministic: prefer an external parameter when the result must be reproducible.

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
