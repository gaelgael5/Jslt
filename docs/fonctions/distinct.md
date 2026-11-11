<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `distinct`

*Français · [English](distinct.en.md)*

Valeurs uniques sélectionnées par un chemin JSONPath dans un tableau, dans l'ordre d'apparition

```
distinct(source, path)
```

**Exemple**

```jslt
{ "r": distinct($.l, $.*) }
```

```json
{ "l": [1, 2, 2, 3] }
```

```json
{ "r": [1, 2, 3] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `path` | optionnel | chemin JSONPath **non évalué** |

**À savoir**

- Le chemin s'applique au **tableau entier** (`$.*.v`), pas à chaque élément — convention inverse de `sort` et `distinctby`, dont la clef est évaluée par élément.
- Pour dédupliquer des **objets** sur une clef, c'est `distinctby`.

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
