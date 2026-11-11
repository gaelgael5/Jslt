<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `difference`

*Français · [English](difference.en.md)*

Éléments du tableau de gauche absents du tableau de droite, dédupliqués

```
difference(left, right)
```

**Exemple**

```jslt
{ "r": difference($.a, $.b) }
```

```json
{ "a": [1, 2, 3], "b": [2] }
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
