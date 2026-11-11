<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datestartof`

*Français · [English](datestartof.en.md)*

Premier instant de la période contenant la date : year, quarter, month, week (lundi), day, hour ou minute

```
datestartof(token, period)
```

**Exemple**

```jslt
{ "r": datestartof($.d, "week") }
```

```json
{ "d": "2026-11-11T09:30:00" }
```

```json
{ "r": "2026-11-09T00:00:00" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `period` | optionnel |  |

**Chapitre** : [Dates et heures](../dates.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
