<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `format`

*Français · [English](format.en.md)*

Formate un nombre ou une date ISO selon un masque (N2, #,##0.00, dd/MM/yyyy…) et une culture

```
format(token, mask, culture)
```

**Exemples**

*Masques de **nombre** : une lettre et une précision. La culture fournit les séparateurs et le symbole.*

```jslt
{ "nombre": format($.n, "N2", "fr-FR"), "pourcent": format($.p, "P0", "fr-FR") }
```

```json
{ "n": 1234.5, "p": 0.25 }
```

```json
{ "nombre": "1 234,50", "pourcent": "25 %" }
```

*Masques de **date** : mêmes jetons qu'à la lecture, et les noms de jours et de mois viennent de la culture.*

```jslt
{ "date": format($.d, "dd/MM/yyyy"), "long": format($.d, "dddd d MMMM yyyy", "fr-FR") }
```

```json
{ "d": "2026-11-11T09:30:00" }
```

```json
{ "date": "11/11/2026", "long": "mercredi 11 novembre 2026" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel | le nombre, ou la date ISO 8601, à écrire |
| `mask` | optionnel | masque de nombre (`N2`, `#,##0.00`…) ou de date (`dd/MM/yyyy`, `dddd d MMMM yyyy`, ou une lettre standard) |
| `culture` | optionnel | séparateurs, symbole monétaire, noms de jours et de mois : `en-US`, `en-GB`, `fr-FR`, `de-DE`, `es-ES`, `it-IT`, ou vide pour l'invariante |

**À savoir**

- Le tableau complet des masques — nombres, dates, cultures — est dans [Formatage](../texte.md#formatage--format).
- Une chaîne **ISO 8601 est une date** : `format($.d, "dd/MM/yyyy")` la formate comme telle, sans conversion préalable.
- La culture décide des séparateurs : `#,##0.00` rend `1 234,50` en `fr-FR` et `1,234.50` en `en-US`. Le masque, lui, ne change pas.
- Un masque hors du sous-ensemble géré **lève**, plutôt que de rendre un texte approximatif qu'on ne verrait qu'en production.

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
