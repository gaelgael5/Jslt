<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `index`

*Français · [English](index.en.md)*

Élément d'un index (créé par createindex) pour une clé, ou null

```
index(index, key)
```

**Exemple**

```jslt
{ "i:": createindex($.p, "", "$.nom"), "ana": index(i:, "Ana") }
```

```json
{ "p": [{ "nom": "Ana", "ville": "Lyon" }] }
```

```json
{ "ana": { "nom": "Ana", "ville": "Lyon" } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `index` | optionnel |  |
| `key` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
