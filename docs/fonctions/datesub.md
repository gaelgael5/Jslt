<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datesub`

*Français · [English](datesub.en.md)*

Retranche une durée à une date ISO 8601 : unité second, minute, hour, day, week, month ou year, et un nombre entier

```
datesub(token, unit, amount)
```

**Exemple**

```jslt
{ "r": datesub($.d, "day", 1) }
```

```json
{ "d": "2026-03-01T00:00:00" }
```

```json
{ "r": "2026-02-28T00:00:00" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel | la date ISO 8601 de départ |
| `unit` | optionnel | `second`, `minute`, `hour`, `day`, `week`, `month` ou `year` (pluriel toléré) |
| `amount` | optionnel | nombre entier |

**Chapitre** : [Dates et heures](../dates.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
