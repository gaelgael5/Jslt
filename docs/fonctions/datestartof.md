<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datestartof`

*Français · [English](datestartof.en.md)*

Premier instant de la période contenant la date : year, quarter, month, week (lundi), day, hour ou minute

```
datestartof(token, period)
```

**Exemple**

*La semaine commence **lundi** : un mercredi est ramené au lundi qui le précède, à minuit.*

```jslt
{ "semaine": datestartof($.d, "week"), "mois": datestartof($.d, "month") }
```

```json
{ "d": "2026-11-11T09:30:00" }
```

```json
{ "semaine": "2026-11-09T00:00:00", "mois": "2026-11-01T00:00:00" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel | la date ISO 8601 à ramener au début de sa période |
| `period` | optionnel | `year`, `quarter`, `month`, `week` (lundi), `day`, `hour` ou `minute` |

**À savoir**

- La semaine commence **lundi** (ISO). Périodes : `year`, `quarter`, `month`, `week`, `day`, `hour`, `minute`.

**Chapitre** : [Dates et heures](../dates.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
