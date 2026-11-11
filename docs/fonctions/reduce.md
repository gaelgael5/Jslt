<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `reduce`

*Français · [English](reduce.en.md)*

Replie un tableau en une seule valeur ; l'expression voit { acc, value, index } et rend le nouvel accumulateur

```
reduce(source, expression, initial)
```

**Exemples**

*L'expression voit `{acc, value, index}` et rend le nouvel accumulateur.*

```jslt
{ "somme": reduce($.l, $.acc + $.value, 0), "colle": reduce($.t, $.acc + $.value, "") }
```

```json
{ "l": [1, 2, 3, 4], "t": ["a", "b", "c"] }
```

```json
{ "somme": 10, "colle": "abc" }
```

*Sans valeur initiale, le repli part du **premier élément**.*

```jslt
{ "r": reduce($.l, max($.acc, $.value)) }
```

```json
{ "l": [3, 9, 2] }
```

```json
{ "r": 9.0 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `expression` | optionnel | expression **non évaluée**, calculée par la fonction |
| `initial` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
