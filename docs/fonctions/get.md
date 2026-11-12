<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `get`

*Français · [English](get.en.md)*

Valeur d'une clef d'objet ou d'un indice de tableau calculés (null si absente)

```
get(token, key)
```

**Exemple**

*La clef vient des **données** : un chemin, lui, est écrit dans le template.*

```jslt
{ "r": get($.o, $.k), "dernier": get($.l, -1) }
```

```json
{ "o": { "a": 1, "b": 2 }, "k": "b", "l": [7, 8, 9] }
```

```json
{ "r": 2, "dernier": 9 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel | l'objet ou le tableau à lire ; autre chose rend `null` |
| `key` | optionnel | la clef, **calculée** : nom pour un objet, indice pour un tableau (négatif depuis la fin) |

**À savoir**

- Clef absente, indice hors bornes, source qui n'est ni objet ni tableau : `null`. Il n'y a donc pas d'argument de repli — `get($.o, $.k) ?? 0` le dit, et un repli en argument serait évalué même quand la clef existe.
- Pour **exiger** la valeur : `require(get($.o, $.k), "tarif inconnu")`. Pour distinguer une clef absente d'une clef présente valant `null` : `has`.

**Chapitre** : [Objets et structures profondes](../objets.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
