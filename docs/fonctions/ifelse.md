<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `ifelse`

*Français · [English](ifelse.en.md)*

Valeur de la 2e expression si la condition est vraie, sinon celle de la 3e (seule la branche retenue est évaluée)

```
ifelse(condition, when_true, when_false)
```

**Exemple**

*La branche écartée n'est **pas** évaluée : la division par zéro ne part pas.*

```jslt
{ "taille": ifelse($.n > 10, "grand", "petit"), "ratio": ifelse($.d == 0, 0, 100 / $.d) }
```

```json
{ "n": 42, "d": 0 }
```

```json
{ "taille": "grand", "ratio": 0 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `condition` | optionnel | l'expression à tester ; lue comme celle de `filter` (`null`, `0`, `""`, vide = faux), pas comme une assertion |
| `when_true` | optionnel | valeur rendue si la condition est vraie ; **non évaluée** sinon · expression **non évaluée**, calculée par la fonction |
| `when_false` | optionnel | valeur rendue sinon ; absente, le résultat est `null` · expression **non évaluée**, calculée par la fonction |

**À savoir**

- Seule la branche **retenue** est évaluée : `ifelse($.d == 0, 0, 100 / $.d)` ne divise pas par zéro. C'est tout l'intérêt de la fonction, et ce qu'un opérateur à arguments évalués ne pourrait pas offrir.
- `when` aiguille sur une **valeur** (`==` contre chaque nom de cas) ; `ifelse` teste une **condition**, donc une expression composée. Pour plus de deux cas, `ifelse` s'imbrique.

**Chapitre** : [Conditions et boucles](../conditions-et-boucles.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
