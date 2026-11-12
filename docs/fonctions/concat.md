<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `concat`

*Français · [English](concat.en.md)*

Joint les éléments d'un tableau en un texte, séparés par split_char suivi de delimit_char (c'est le « join » des textes ; join, lui, est la jointure)

```
concat(token, split_char, delimit_char)
```

**Exemple**

```jslt
{ "colle": concat($.l), "joint": concat($.l, "-") }
```

```json
{ "l": ["a", "b", "c"] }
```

```json
{ "colle": "abc", "joint": "a-b-c" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `split_char` | optionnel |  |
| `delimit_char` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
