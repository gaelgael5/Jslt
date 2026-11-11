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

**Chapter**: [Quality: refuse, observe, validate](../qualite.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
