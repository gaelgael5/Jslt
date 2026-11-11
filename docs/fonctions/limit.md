<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `limit`

*Français · [English](limit.en.md)*

Les max_items premiers éléments d'un tableau

```
limit(source, max_items)
```

**Exemple**

```jslt
{ "r": limit($.l, 2) }
```

```json
{ "l": [1, 2, 3, 4] }
```

```json
{ "r": [1, 2] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `max_items` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
