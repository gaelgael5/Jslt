<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `select`

*Français · [English](select.en.md)*

Première valeur sélectionnée par un chemin JSONPath dans la source, ou null

```
select(source, path)
```

**Exemple**

```jslt
{ "r": select($.d, $.client.nom) }
```

```json
{ "d": { "client": { "nom": "Ana" } } }
```

```json
{ "r": "Ana" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `path` | optionnel | chemin JSONPath **non évalué** |

**À savoir**

- Le 2e argument est un **argument-chemin** : il n'est pas évalué comme une expression, il est appliqué à `source`. Il s'écrit aussi en chaîne (`"$.client.nom"`).
- Plusieurs valeurs trouvées : c'est la **première**. Aucune : `null`.

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
