<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `dateendof`

*Français · [English](dateendof.en.md)*

Dernier instant de la période contenant la date (borne inclusive, à la microseconde près)

```
dateendof(token, period)
```

**Exemple**

*Borne **inclusive** : la dernière microseconde de la période, pour qu'un filtre `<=` attrape toute la journée (ou tout le mois).*

```jslt
{ "mois": dateendof($.d, "month"), "jour": dateendof($.d, "day") }
```

```json
{ "d": "2026-02-10T12:00:00" }
```

```json
{ "mois": "2026-02-28T23:59:59.999999", "jour": "2026-02-10T23:59:59.999999" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel | la date ISO 8601 à porter à la fin de sa période |
| `period` | optionnel | `year`, `quarter`, `month`, `week`, `day`, `hour` ou `minute` |

**À savoir**

- La borne est **inclusive**, à la microseconde près : la fin d'un jour est `23:59:59.999999`, et non le début du lendemain. Un filtre `<=` attrape donc toute la journée.

**Chapitre** : [Dates et heures](../dates.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
