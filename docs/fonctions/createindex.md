<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `createindex`

*Français · [English](createindex.en.md)*

Construit un index {clé: élément} à partir d'une source, d'un chemin de découpe et d'un chemin de clé

```
createindex(source, object_path, key)
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
| `source` | optionnel |  |
| `object_path` | optionnel |  |
| `key` | optionnel |  |

**À savoir**

- Se range dans une variable (`"i:": createindex(…)`) que `index(i:, clé)` interroge ensuite. Le 2e argument est le chemin de **découpe** (vide = la source entière).

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
