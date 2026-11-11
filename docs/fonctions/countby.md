<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `countby`

*Français · [English](countby.en.md)*

Compte les éléments d'un tableau par clef calculée, en un objet { clef: nombre }

```
countby(source, key)
```

**Exemple**

```jslt
{ "r": countby($.l, $.ville) }
```

```json
{ "l": [{ "ville": "Lyon" }, { "ville": "Lyon" }, { "ville": "Brest" }] }
```

```json
{ "r": { "Lyon": 2, "Brest": 1 } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `key` | optionnel | expression **non évaluée**, calculée par la fonction |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
