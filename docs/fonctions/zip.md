<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `zip`

*Français · [English](zip.en.md)*

Apparie deux tableaux élément par élément, en s'arrêtant au plus court

```
zip(left, right)
```

**Exemple**

```jslt
{ "r": zip($.a, $.b) }
```

```json
{ "a": [1, 2], "b": ["x", "y"] }
```

```json
{ "r": [[1, "x"], [2, "y"]] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `left` | optionnel |  |
| `right` | optionnel |  |

**À savoir**

- S'arrête au plus court plutôt que de compléter par `null` : un appariement inventé serait indiscernable d'une vraie valeur nulle.

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
