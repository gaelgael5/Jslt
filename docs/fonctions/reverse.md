<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `reverse`

*Français · [English](reverse.en.md)*

Inverse l'ordre d'un tableau ou d'un texte, sans modifier la source

```
reverse(source)
```

**Exemple**

```jslt
{ "tableau": reverse($.l), "texte": reverse($.t) }
```

```json
{ "l": [1, 2, 3], "t": "abc" }
```

```json
{ "tableau": [3, 2, 1], "texte": "cba" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
