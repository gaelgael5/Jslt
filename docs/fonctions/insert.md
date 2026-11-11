<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `insert`

*Français · [English](insert.en.md)*

Copie du tableau avec une valeur insérée à l'indice donné (négatif depuis la fin)

```
insert(source, index, value)
```

**Exemple**

```jslt
{ "debut": insert($.l, 0, 9), "avant_dernier": insert($.l, -1, 9) }
```

```json
{ "l": [1, 2] }
```

```json
{ "debut": [9, 1, 2], "avant_dernier": [1, 9, 2] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `index` | optionnel |  |
| `value` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
