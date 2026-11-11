<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `max`

*Français · [English](max.en.md)*

Plus grand de deux nombres, ou du tableau donné (décimal pour deux nombres)

```
max(left, right)
```

**Exemple**

```jslt
{ "deux": max($.a, $.b), "du_tableau": max($.l) }
```

```json
{ "a": 2, "b": 9, "l": [3, 11, 7] }
```

```json
{ "deux": 9.0, "du_tableau": 11 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `left` | optionnel |  |
| `right` | optionnel |  |

**À savoir**

- Deux formes : deux nombres (résultat **décimal**) ou un tableau (le **type est conservé**). Un tableau *et* un second argument lève.

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
