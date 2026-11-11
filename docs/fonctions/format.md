<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `format`

*Français · [English](format.en.md)*

Formate un nombre ou une date (chaîne ISO) avec un masque .NET et une culture

```
format(token, mask, culture)
```

**Exemples**

```jslt
{ "nombre": format($.n, "N2", "fr-FR"), "pourcent": format($.p, "P0", "fr-FR") }
```

```json
{ "n": 1234.5, "p": 0.25 }
```

```json
{ "nombre": "1 234,50", "pourcent": "25 %" }
```

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
| `token` | optionnel |  |
| `mask` | optionnel |  |
| `culture` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
