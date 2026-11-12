<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `every`

*Français · [English](every.en.md)*

Vrai si le prédicat est vrai pour tous les éléments (vrai pour un tableau vide)

```
every(source, predicate)
```

**Exemple**

*Vrai sur un tableau **vide** : il n'y a aucun contre-exemple.*

```jslt
{ "tous": every($.l, $ > 0), "vide": every($.v, $ > 0) }
```

```json
{ "l": [1, 2], "v": [] }
```

```json
{ "tous": true, "vide": true }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `predicate` | optionnel | expression **non évaluée**, calculée par la fonction |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
