<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datepart`

*Français · [English](datepart.en.md)*

Extrait une composante entière d'une date ISO 8601 : year, month, day, dayofweek (dimanche = 0), hour, minute ou second

```
datepart(token, part)
```

**Exemple**

```jslt
{ "annee": datepart($.d, "year"), "jour_semaine": datepart($.d, "dayofweek") }
```

```json
{ "d": "2026-11-11T09:30:00" }
```

```json
{ "annee": 2026, "jour_semaine": 3 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `part` | optionnel |  |

**Chapitre** : [Dates et heures](../dates.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
