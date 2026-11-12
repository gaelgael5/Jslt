<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `filter`

*Français · [English](filter.en.md)*

Garde les éléments d'un tableau pour lesquels le prédicat est vrai

```
filter(source, predicate)
```

**Exemple**

*L'expression est quelconque : un filtre JSONPath ne sait pas appeler une fonction.*

```jslt
{ "r": filter($.l, stringcontains($.n, "a")) }
```

```json
{ "l": [{ "n": "Ana" }, { "n": "Bo" }] }
```

```json
{ "r": [{ "n": "Ana" }] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `predicate` | optionnel | expression **non évaluée**, calculée par la fonction |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
