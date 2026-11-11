<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `min`

*Français · [English](min.en.md)*

Plus petit de deux nombres, ou du tableau donné (décimal pour deux nombres)

```
min(left, right)
```

**Exemple**

```jslt
{ "deux": min($.a, $.b), "du_tableau": min($.l) }
```

```json
{ "a": 2, "b": 9, "l": [3, 11, 7] }
```

```json
{ "deux": 2.0, "du_tableau": 3 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `left` | optionnel |  |
| `right` | optionnel |  |

**À savoir**

- Deux formes : deux nombres (résultat **décimal**) ou un tableau (le **type est conservé**). Un tableau *et* un second argument lève, plutôt que d'ignorer le second.

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
