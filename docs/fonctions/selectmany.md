<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `selectmany`

*Français · [English](selectmany.en.md)*

Toutes les valeurs sélectionnées par un chemin JSONPath dans la source

```
selectmany(source, path)
```

**Exemple**

```jslt
{ "r": selectmany($.l, $.*.id) }
```

```json
{ "l": [{ "id": 1 }, { "id": 2 }] }
```

```json
{ "r": [1, 2] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `path` | optionnel | chemin JSONPath **non évalué** |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
