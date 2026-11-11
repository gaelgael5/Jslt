<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `skip`

*Français · [English](skip.en.md)*

Ignore les n premiers éléments d'un tableau (complément de limit)

```
skip(source, count)
```

**Exemple**

```jslt
{ "r": skip($.l, 2) }
```

```json
{ "l": [1, 2, 3, 4] }
```

```json
{ "r": [3, 4] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `count` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
