<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `any`

*Français · [English](any.en.md)*

Vrai si la source est un tableau non vide

```
any(source)
```

**Exemple**

```jslt
{ "pleine": any($.l), "vide": any($.v) }
```

```json
{ "l": [1], "v": [] }
```

```json
{ "pleine": true, "vide": false }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
