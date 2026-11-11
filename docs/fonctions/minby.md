<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `minby`

*Français · [English](minby.en.md)*

Élément d'un tableau dont la clef calculée est la plus petite (null si vide)

```
minby(source, key)
```

**Exemple**

*Rend l'**élément**, là où `min` rend la valeur extrême sans dire qui la porte.*

```jslt
{ "r": map([minby($.l, $.prix)], $.ref) }
```

```json
{ "l": [{ "ref": "A", "prix": 30 }, { "ref": "B", "prix": 10 }] }
```

```json
{ "r": ["B"] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `key` | optionnel | expression **non évaluée**, calculée par la fonction |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
