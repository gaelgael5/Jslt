<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `range`

*Français · [English](range.en.md)*

Série d'entiers : range(fin), range(début, fin) ou range(début, fin, pas) ; la fin est exclue

```
range(start, end, step)
```

**Exemples**

*La **fin est exclue**, et un seul argument compte depuis zéro.*

```jslt
{ "depuis_zero": range(5), "bornes": range(2, 5), "pas": range(0, 10, 3), "descendant": range(3, 0, -1) }
```

```json
{}
```

```json
{ "depuis_zero": [0, 1, 2, 3, 4], "bornes": [2, 3, 4], "pas": [0, 3, 6, 9], "descendant": [3, 2, 1] }
```

*Seule fonction qui **crée** une série : tout le reste transforme ce qui entre.*

```jslt
{ "carres": map(range(1, 5), $ * $) }
```

```json
{}
```

```json
{ "carres": [1, 4, 9, 16] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `start` | optionnel |  |
| `end` | optionnel |  |
| `step` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
