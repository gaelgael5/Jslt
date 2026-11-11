<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datepart`

*Français · [English](datepart.en.md)*

Extrait une composante entière d'une date ISO 8601 : year, month, day, dayofweek (dimanche = 0), hour, minute ou second

```
datepart(token, part)
```

**Exemple**

*`dayofweek` compte à partir de **dimanche = 0** : le 11 novembre 2026 est un mercredi, donc 3.*

```jslt
{ "annee": datepart($.d, "year"), "trimestre": datepart($.d, "quarter"), "jour_semaine": datepart($.d, "dayofweek") }
```

```json
{ "d": "2026-11-11T09:30:00" }
```

```json
{ "annee": 2026, "trimestre": 4, "jour_semaine": 3 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel | la date ISO 8601 à décomposer |
| `part` | optionnel | `year`, `quarter`, `month`, `day`, `dayofweek`, `dayofyear`, `week`, `hour`, `minute` ou `second` |

**À savoir**

- `dayofweek` numérote à partir de **dimanche = 0** (samedi = 6), alors que `datestartof(…, "week")` commence **lundi** (ISO). Les deux conventions coexistent : la première nomme un jour, la seconde borne une semaine.
- Parties disponibles : `year`, `quarter`, `month`, `day`, `dayofweek`, `dayofyear`, `week`, `hour`, `minute`, `second`.

**Chapitre** : [Dates et heures](../dates.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
