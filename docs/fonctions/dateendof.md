<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `dateendof`

*Français · [English](dateendof.en.md)*

Dernier instant de la période contenant la date (borne inclusive, à la microseconde près)

```
dateendof(token, period)
```

**Exemple**

```jslt
{ "r": dateendof($.d, "month") }
```

```json
{ "d": "2026-02-10T12:00:00" }
```

```json
{ "r": "2026-02-28T23:59:59.999999" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `period` | optionnel |  |

**Chapitre** : [Dates et heures](../dates.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
