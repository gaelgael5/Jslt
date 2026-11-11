<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `contains`

*Français · [English](contains.en.md)*

Vrai si le tableau contient un élément égal à la valeur

```
contains(source, to_match)
```

**Exemple**

```jslt
{ "r": contains($.l, "b") }
```

```json
{ "l": ["a", "b"] }
```

```json
{ "r": true }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `to_match` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
