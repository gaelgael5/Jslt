<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `walk`

*Français · [English](walk.en.md)*

Applique une expression à chaque nœud d'une structure, des feuilles vers la racine

```
walk(token, expression)
```

**Exemple**

```jslt
{ "r": walk($.o, when(isstring($)) { "True": upper($), "default": $ }) }
```

```json
{ "o": { "a": "x", "b": { "c": "y" } } }
```

```json
{ "r": { "a": "X", "b": { "c": "Y" } } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `expression` | optionnel | expression **non évaluée**, calculée par la fonction |

**À savoir**

- Le parcours va des **feuilles vers la racine** : l'expression voit des enfants déjà transformés, donc une règle qui dépend d'eux fonctionne.

**Chapitre** : [Objets et structures profondes](../objets.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
