<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `sumby`

*Français · [English](sumby.en.md)*

Somme par clef calculée, en un objet { clef: somme } (la valeur par défaut est l'élément)

```
sumby(source, key, value)
```

**Exemple**

```jslt
{ "r": sumby($.l, $.ville, $.m) }
```

```json
{ "l": [{ "ville": "Lyon", "m": 10 }, { "ville": "Lyon", "m": 5 }, { "ville": "Brest", "m": 7 }] }
```

```json
{ "r": { "Lyon": 15, "Brest": 7 } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `key` | optionnel | expression **non évaluée**, calculée par la fonction |
| `value` | optionnel | expression **non évaluée**, calculée par la fonction |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
