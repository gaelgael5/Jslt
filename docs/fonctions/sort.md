<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `sort`

*Français · [English](sort.en.md)*

Trie un tableau : sur les éléments, ou sur une clef calculée par élément, du plus petit au plus grand (descending à true, ou un sens par clef, pour l'inverse)

```
sort(source, key, descending)
```

**Exemples**

```jslt
{ "par_prix": selectmany(sort($.l, $.prix), $.*.id) }
```

```json
{ "l": [{ "id": 1, "prix": 30 }, { "id": 2, "prix": 10 }] }
```

```json
{ "par_prix": [2, 1] }
```

```jslt
{ "ville_puis_prix_decroissant": selectmany(sort($.l, [$.ville, $.prix], [false, true]), $.*.id) }
```

```json
{ "l": [{ "id": 1, "ville": "Lyon", "prix": 10 }, { "id": 2, "ville": "Lyon", "prix": 30 }, { "id": 3, "ville": "Brest", "prix": 5 }] }
```

```json
{ "ville_puis_prix_decroissant": [3, 2, 1] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel | le tableau à trier |
| `key` | optionnel | expression évaluée **par élément** (`$.prix`), un tableau pour trier sur plusieurs critères, ou rien pour trier les éléments eux-mêmes · expression **non évaluée**, calculée par la fonction |
| `descending` | optionnel | `true` pour l'ordre inverse, ou un **tableau de booléens** : un sens par clef |

**À savoir**

- L'ordre est **total** et ne lève jamais : `null` < booléens < nombres < chaînes < tableaux < objets. Les chaînes se comparent par **points de code** — pour un ordre humain, trier sur `foldtext($)`.
- Le tri est **stable** dans les deux sens : à clefs égales, l'ordre d'origine survit.

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
