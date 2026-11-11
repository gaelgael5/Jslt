<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isiban`

*[Français](isiban.md) · English*

True when the text is an IBAN whose check digits (modulo 97) are right

```
isiban(token)
```

**Example**

```jslt
{ "r": isiban($.t) }
```

```json
{ "t": "FR7630006000011234567890189" }
```

```json
{ "r": true }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Good to know**

- Checks the structure and the **modulo-97 check digits**, but not the per-country length: that would be a sixty-entry table whose staleness would reject a valid IBAN.

**Chapter**: [Quality: refuse, observe, validate](../qualite.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
