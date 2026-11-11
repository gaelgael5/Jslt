<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `findindex`

*Français · [English](findindex.en.md)*

Position du premier élément qui satisfait le prédicat, -1 si aucun

```
findindex(source, predicate)
```

**Exemple**

```jslt
{ "position": findindex($.l, $ > 2), "aucune": findindex($.l, $ > 9) }
```

```json
{ "l": [1, 2, 3, 4] }
```

```json
{ "position": 2, "aucune": -1 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `predicate` | optionnel | expression **non évaluée**, calculée par la fonction |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
