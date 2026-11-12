<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `removeat`

*Français · [English](removeat.en.md)*

Copie du tableau privée de l'élément à l'indice donné (négatif depuis la fin)

```
removeat(source, index)
```

**Exemple**

*Un indice hors bornes rend la copie **inchangée**, il ne lève pas.*

```jslt
{ "sans_le_second": removeat($.l, 1), "dernier": removeat($.l, -1), "hors_bornes": removeat($.l, 9) }
```

```json
{ "l": [1, 2, 3] }
```

```json
{ "sans_le_second": [1, 3], "dernier": [1, 2], "hors_bornes": [1, 2, 3] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `index` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
