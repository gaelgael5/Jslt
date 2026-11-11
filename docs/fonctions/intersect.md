<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `intersect`

*Français · [English](intersect.en.md)*

Éléments du tableau de gauche présents aussi à droite, dédupliqués

```
intersect(left, right)
```

**Exemple**

```jslt
{ "r": intersect($.a, $.b) }
```

```json
{ "a": [1, 2, 3], "b": [3, 1] }
```

```json
{ "r": [1, 3] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `left` | optionnel |  |
| `right` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
