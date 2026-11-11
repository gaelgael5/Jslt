<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `avgby`

*Français · [English](avgby.en.md)*

Moyenne par clef calculée, en un objet { clef: moyenne } (la valeur par défaut est l'élément)

```
avgby(source, key, value)
```

**Exemple**

```jslt
{ "r": avgby($.l, $.ville, $.m) }
```

```json
{ "l": [{ "ville": "Lyon", "m": 10 }, { "ville": "Lyon", "m": 20 }, { "ville": "Brest", "m": 7 }] }
```

```json
{ "r": { "Lyon": 15.0, "Brest": 7.0 } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `key` | optionnel | expression **non évaluée**, calculée par la fonction |
| `value` | optionnel | expression **non évaluée**, calculée par la fonction |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
