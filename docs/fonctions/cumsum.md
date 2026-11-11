<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `cumsum`

*Français · [English](cumsum.en.md)*

Totaux courants d'un tableau de nombres ([1,2,3] -> [1,3,6])

```
cumsum(source)
```

**Exemple**

```jslt
{ "r": cumsum($.l) }
```

```json
{ "l": [1, 2, 3, 4] }
```

```json
{ "r": [1, 3, 6, 10] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
