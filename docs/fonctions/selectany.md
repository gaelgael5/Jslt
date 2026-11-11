<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `selectany`

*Français · [English](selectany.en.md)*

Vrai si le chemin JSONPath sélectionne au moins une valeur dans la source

```
selectany(source, path)
```

**Exemple**

```jslt
{ "r": selectany($.d, $.client.nom) }
```

```json
{ "d": { "client": { "nom": "Ana" } } }
```

```json
{ "r": true }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `path` | optionnel | chemin JSONPath **non évalué** |

**À savoir**

- Compte les **nœuds** sélectionnés, pas leur vérité : une valeur `0` ou `""` trouvée rend `true`.

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
