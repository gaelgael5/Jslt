<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `parsedate`

*Français · [English](parsedate.en.md)*

Lit une date texte et la rend en ISO 8601 : détection selon la culture, ou masque explicite (dd/MM/yyyy…), avec un fuseau optionnel

```
parsedate(token, culture, mask, timezone)
```

**Exemple**

```jslt
{ "culture": parsedate($.a, "fr-FR"), "masque": parsedate($.b, "", "dd/MM/yyyy") }
```

```json
{ "a": "11/11/2026", "b": "11/11/2026" }
```

```json
{ "culture": "2026-11-11T00:00:00", "masque": "2026-11-11T00:00:00" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `culture` | optionnel |  |
| `mask` | optionnel |  |
| `timezone` | optionnel |  |

**Chapitre** : [Dates et heures](../dates.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
