<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `merge`

*Français · [English](merge.en.md)*

Fusionne deux objets, la droite gagnant les clés communes (deep pour les sous-objets, arrays pour concaténer les tableaux)

```
merge(left, right, deep, arrays)
```

**Exemple**

```jslt
{ "r": merge($.a, $.b) }
```

```json
{ "a": { "x": 1, "y": 2 }, "b": { "y": 9 } }
```

```json
{ "r": { "x": 1, "y": 9 } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `left` | optionnel |  |
| `right` | optionnel |  |
| `deep` | optionnel |  |
| `arrays` | optionnel |  |

**Chapitre** : [Objets et structures profondes](../objets.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
