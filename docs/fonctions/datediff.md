<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datediff`

*Français · [English](datediff.en.md)*

Compte les unités entières écoulées entre deux dates ISO 8601 : second, minute, hour, day, week, month ou year, négatif si la fin précède le début

```
datediff(start, end, unit)
```

**Exemple**

```jslt
{ "jours": datediff($.a, $.b, "day") }
```

```json
{ "a": "2026-11-01T00:00:00", "b": "2026-11-11T00:00:00" }
```

```json
{ "jours": 10 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `start` | optionnel |  |
| `end` | optionnel |  |
| `unit` | optionnel |  |

**Chapitre** : [Dates et heures](../dates.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
