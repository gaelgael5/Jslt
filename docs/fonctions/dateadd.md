<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `dateadd`

*Français · [English](dateadd.en.md)*

Ajoute une durée à une date ISO 8601 : unité second, minute, hour, day, week, month ou year, et un nombre entier (négatif pour retrancher)

```
dateadd(token, unit, amount)
```

**Exemples**

*Ajouter, et retrancher avec un nombre négatif.*

```jslt
{ "dans_deux_mois": dateadd($.d, "month", 2), "hier": dateadd($.d, "day", -1) }
```

```json
{ "d": "2026-01-15T00:00:00" }
```

```json
{ "dans_deux_mois": "2026-03-15T00:00:00", "hier": "2026-01-14T00:00:00" }
```

*`month` est **calendaire** : le 31 janvier + 1 mois donne le 28 février, borné sur le mois court — et non le 3 mars.*

```jslt
{ "borne": dateadd($.d, "month", 1) }
```

```json
{ "d": "2026-01-31T00:00:00" }
```

```json
{ "borne": "2026-02-28T00:00:00" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel | la date ISO 8601 de départ |
| `unit` | optionnel | `second`, `minute`, `hour`, `day`, `week`, `month` ou `year` (pluriel toléré) |
| `amount` | optionnel | nombre entier, négatif pour retrancher |

**À savoir**

- `month` et `year` sont **calendaires** : le jour est **borné** sur les mois courts, donc le 31 janvier + 1 mois donne le 28 février, et non le 3 mars.
- Conséquence : `dateadd` et `datediff` ne sont **pas** exactement inverses l'un de l'autre sur ces deux unités.

**Chapitre** : [Dates et heures](../dates.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
