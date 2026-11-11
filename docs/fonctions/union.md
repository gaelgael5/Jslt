<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `union`

*Français · [English](union.en.md)*

Aplatit d'un niveau un tableau de tableaux

```
union(source)
```

**Exemple**

```jslt
{ "r": union($.l) }
```

```json
{ "l": [[1, 2], [3]] }
```

```json
{ "r": [1, 2, 3] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
