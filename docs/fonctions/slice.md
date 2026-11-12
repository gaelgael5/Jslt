<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `slice`

*Français · [English](slice.en.md)*

Tranche d'un tableau de start à end exclu (indices négatifs depuis la fin)

```
slice(source, start, end)
```

**Exemple**

*Fin exclue, indices négatifs depuis la fin, bornes trop larges tolérées.*

```jslt
{ "milieu": slice($.l, 1, 3), "fin": slice($.l, -2), "trop_loin": slice($.l, 9) }
```

```json
{ "l": [1, 2, 3, 4, 5] }
```

```json
{ "milieu": [2, 3], "fin": [4, 5], "trop_loin": [] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `start` | optionnel |  |
| `end` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
