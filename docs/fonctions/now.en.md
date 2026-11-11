<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `now`

*[Français](now.md) · English*

Current date and time in ISO 8601: local, or UTC when utc is true

```
now(utc)
```

**Example**

```jslt
{ "r": datepart(now(), "year") >= 2026 }
```

```json
{}
```

```json
{ "r": true }
```

| Parameter | Expected | Note |
|---|---|---|
| `utc` | optional |  |

**Good to know**

- Non-deterministic: two calls in the same template may differ. For a **testable** template, pass the instant as an external parameter (`param("reference_date")`) rather than calling `now()`.

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
