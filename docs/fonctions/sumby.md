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
| `source` | optionnel | le tableau à agréger |
| `key` | optionnel | expression de la clef de groupe, évaluée par élément · expression **non évaluée**, calculée par la fonction |
| `value` | optionnel | expression de la valeur à sommer ; omise, c'est l'élément · expression **non évaluée**, calculée par la fonction |

**À savoir**

- Une valeur non numérique **lève**, comme pour `sum` : un total qui saute les intrus est plausible et faux.

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
