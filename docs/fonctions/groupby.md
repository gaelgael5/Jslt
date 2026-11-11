<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `groupby`

*Français · [English](groupby.en.md)*

Regroupe un tableau en un objet { clef: éléments }, clef calculée par élément ; nested imbrique un niveau par clef d'un tableau de clefs

```
groupby(source, key, nested)
```

**Exemples**

```jslt
{ "plat": groupby($.l, $.ville) }
```

```json
{ "l": [{ "id": 1, "ville": "Lyon" }, { "id": 2, "ville": "Brest" }] }
```

```json
{ "plat": { "Lyon": [{ "id": 1, "ville": "Lyon" }], "Brest": [{ "id": 2, "ville": "Brest" }] } }
```

```jslt
{ "imbrique": groupby($.l, [$.pays, $.ville], true) }
```

```json
{ "l": [{ "id": 1, "pays": "FR", "ville": "Lyon" }] }
```

```json
{ "imbrique": { "FR": { "Lyon": [{ "id": 1, "pays": "FR", "ville": "Lyon" }] } } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel | le tableau à regrouper |
| `key` | optionnel | expression évaluée **par élément** ; un tableau pour une clef composite · expression **non évaluée**, calculée par la fonction |
| `nested` | optionnel | `true` pour imbriquer un niveau d'objet par clef |

**À savoir**

- La clef est convertie en **texte**, puisqu'une clé d'objet JSON est une chaîne : une clef composite donne `["FR","Lyon"]` en JSON compact. `nested` évite d'avoir à la re-analyser.

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
