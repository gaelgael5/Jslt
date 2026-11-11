<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `count`

*Français · [English](count.en.md)*

Nombre d'éléments : éléments d'un tableau, clés d'un objet, caractères d'un texte, 0 pour null

```
count(token)
```

**Exemple**

```jslt
{ "tableau": count($.l), "objet": count($.o), "texte": count($.t) }
```

```json
{ "l": [1, 2], "o": { "a": 1 }, "t": "abc" }
```

```json
{ "tableau": 2, "objet": 1, "texte": 3 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**À savoir**

- Compte les éléments d'un tableau, les **clés** d'un objet, les **caractères** d'un texte ; un scalaire vaut 1 (c'est une valeur) et `null` vaut 0 (c'est une absence).

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
