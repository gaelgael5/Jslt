<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isemail`

*[Français](isemail.md) · English*

True when the text has the shape of an email address

```
isemail(token)
```

**Example**

```jslt
{ "r": isemail($.t) }
```

```json
{ "t": "ana@exemple.fr" }
```

```json
{ "r": true }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Good to know**

- Deliberately **pragmatic**: the full RFC 5322 accepts forms nobody uses, and accepting them would let through what a downstream system will reject.

**Chapter**: [Quality: refuse, observe, validate](../qualite.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
