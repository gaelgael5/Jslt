<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `distinctby`

*Français · [English](distinctby.en.md)*

Déduplique un tableau sur une clef calculée par élément, en gardant le premier

```
distinctby(source, key)
```

**Exemple**

```jslt
{ "r": distinctby($.l, $.ville) }
```

```json
{ "l": [{ "id": 1, "ville": "Lyon" }, { "id": 2, "ville": "Lyon" }, { "id": 3, "ville": "Brest" }] }
```

```json
{ "r": [{ "id": 1, "ville": "Lyon" }, { "id": 3, "ville": "Brest" }] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `key` | optionnel | expression **non évaluée**, calculée par la fonction |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
