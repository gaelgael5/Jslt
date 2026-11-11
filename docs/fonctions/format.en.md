<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `format`

*[Français](format.md) · English*

Formats a number or an ISO date according to a mask (N2, #,##0.00, dd/MM/yyyy…) and a culture

```
format(token, mask, culture)
```

**Examples**

***Number** masks: a letter and a precision. The culture provides the separators and the symbol.*

```jslt
{ "nombre": format($.n, "N2", "fr-FR"), "pourcent": format($.p, "P0", "fr-FR") }
```

```json
{ "n": 1234.5, "p": 0.25 }
```

```json
{ "nombre": "1 234,50", "pourcent": "25 %" }
```

***Date** masks: the same tokens as for reading, and the day and month names come from the culture.*

```jslt
{ "date": format($.d, "dd/MM/yyyy"), "long": format($.d, "dddd d MMMM yyyy", "fr-FR") }
```

```json
{ "d": "2026-11-11T09:30:00" }
```

```json
{ "date": "11/11/2026", "long": "mercredi 11 novembre 2026" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional | the number, or ISO 8601 date, to write |
| `mask` | optional | number mask (`N2`, `#,##0.00`…) or date mask (`dd/MM/yyyy`, `dddd d MMMM yyyy`, or a standard letter) |
| `culture` | optional | separators, currency symbol, day and month names: `en-US`, `en-GB`, `fr-FR`, `de-DE`, `es-ES`, `it-IT`, or empty for the invariant one |

**Good to know**

- The full mask table — numbers, dates, cultures — is in [Formatting](../texte.en.md#formatting-format).
- An **ISO 8601 string is a date**: `format($.d, "dd/MM/yyyy")` formats it as such, with no prior conversion.
- The culture decides the separators: `#,##0.00` returns `1 234,50` in `fr-FR` and `1,234.50` in `en-US`. The mask itself does not change.
- A mask outside the supported subset **raises**, rather than returning an approximate text that would only be noticed in production.

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
