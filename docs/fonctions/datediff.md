<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datediff`

*Français · [English](datediff.en.md)*

Compte les unités entières écoulées entre deux dates ISO 8601 : second, minute, hour, day, week, month ou year, négatif si la fin précède le début

```
datediff(start, end, unit)
```

**Exemples**

*Des unités **entières** écoulées, négatives si la fin précède le début.*

```jslt
{ "jours": datediff($.a, $.b, "day"), "a_rebours": datediff($.b, $.a, "day") }
```

```json
{ "a": "2026-11-01T00:00:00", "b": "2026-11-11T00:00:00" }
```

```json
{ "jours": 10, "a_rebours": -10 }
```

*Un mois n'est compté que lorsque le **jour** de la fin a rattrapé celui du début : du 15 janvier au 14 février, il y en a zéro.*

```jslt
{ "veille": datediff($.a, $.b, "month"), "jour_meme": datediff($.a, $.c, "month") }
```

```json
{ "a": "2026-01-15T00:00:00", "b": "2026-02-14T00:00:00", "c": "2026-02-15T00:00:00" }
```

```json
{ "veille": 0, "jour_meme": 1 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `start` | optionnel | date ISO 8601 de début |
| `end` | optionnel | date ISO 8601 de fin ; avant le début, le résultat est négatif |
| `unit` | optionnel | `second`, `minute`, `hour`, `day`, `week`, `month` ou `year` |

**À savoir**

- Le compte est en unités **entières écoulées**, tronquées **vers zéro** : du 15 janvier au 14 février il y a `0` mois, et au 15 février `1`.
- Comparer une date **avec** fuseau à une date **sans** fuseau lève : l'écart n'aurait pas de sens, et le supposer donnerait un résultat faux de quelques heures.

**Chapitre** : [Dates et heures](../dates.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
