<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `flatten`

*Français · [English](flatten.en.md)*

Aplatit un tableau de tableaux, à fond par défaut ou sur depth niveaux

```
flatten(source, depth)
```

**Exemple**

```jslt
{ "a_fond": flatten($.l), "un_niveau": flatten($.l, 1) }
```

```json
{ "l": [1, [2, [3]]] }
```

```json
{ "a_fond": [1, 2, 3], "un_niveau": [1, 2, [3]] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `depth` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
