<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `map`

*Français · [English](map.en.md)*

Applique une expression à chaque élément d'un tableau et rend les résultats

```
map(source, expression)
```

**Exemple**

*Ce que la boucle fait déjà — mais utilisable **en argument**.*

```jslt
{ "noms": map($.l, $.n), "total": sum(map($.l, $.age)) }
```

```json
{ "l": [{ "n": "Ana", "age": 30 }, { "n": "Bo", "age": 25 }] }
```

```json
{ "noms": ["Ana", "Bo"], "total": 55 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `expression` | optionnel | expression **non évaluée**, calculée par la fonction |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
