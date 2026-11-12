<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `maxby`

*Français · [English](maxby.en.md)*

Élément d'un tableau dont la clef calculée est la plus grande (null si vide)

```
maxby(source, key)
```

**Exemple**

```jslt
{ "r": map([maxby($.l, $.prix)], $.ref) }
```

```json
{ "l": [{ "ref": "A", "prix": 30 }, { "ref": "B", "prix": 10 }] }
```

```json
{ "r": ["A"] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `key` | optionnel | expression **non évaluée**, calculée par la fonction |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
