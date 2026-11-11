<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `dateduration`

*Français · [English](dateduration.en.md)*

Décompose l'intervalle entre deux dates en années, mois, jours, heures, minutes et secondes

```
dateduration(start, end)
```

**Exemple**

*L'intervalle décomposé en valeurs **positives** ; `negative` dit dans quel sens il va.*

```jslt
{ "r": dateduration($.a, $.b) }
```

```json
{ "a": "2026-01-01T00:00:00", "b": "2027-03-02T04:05:06" }
```

```json
{ "r": { "negative": false, "years": 1, "months": 2, "days": 1, "hours": 4, "minutes": 5, "seconds": 6 } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `start` | optionnel |  |
| `end` | optionnel |  |

**À savoir**

- Le résultat porte `negative` : l'intervalle est décomposé en valeurs positives, et c'est ce drapeau qui dit dans quel sens il va.

**Chapitre** : [Dates et heures](../dates.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
