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
| `source` | optionnel |  |
| `key` | optionnel | expression **non évaluée**, calculée par la fonction |
| `nested` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
