<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `find`

*Français · [English](find.en.md)*

Premier élément d'un tableau pour lequel le prédicat est vrai, sinon null

```
find(source, predicate)
```

**Exemple**

```jslt
{ "trouve": find($.l, $ > 2), "aucun": find($.l, $ > 9) }
```

```json
{ "l": [1, 2, 3, 4] }
```

```json
{ "trouve": 3, "aucun": null }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `predicate` | optionnel | expression **non évaluée**, calculée par la fonction |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
