<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `some`

*Français · [English](some.en.md)*

Vrai si le prédicat est vrai pour au moins un élément (faux pour un tableau vide)

```
some(source, predicate)
```

**Exemple**

*`any` dit « tableau non vide » ; `some` teste un prédicat.*

```jslt
{ "some": some($.l, $ > 3), "any": any($.l) }
```

```json
{ "l": [1, 2] }
```

```json
{ "some": false, "any": true }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `predicate` | optionnel | expression **non évaluée**, calculée par la fonction |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
