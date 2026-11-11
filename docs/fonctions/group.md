<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `group`

*Français · [English](group.en.md)*

Regroupe un tableau par chemins JSONPath successifs en {Label, Items} imbriqués

```
group(source, group_paths)
```

**Exemple**

```jslt
{ "r": group($.p, ["$.ville"]) }
```

```json
{ "p": [{ "nom": "Ana", "ville": "Lyon" }] }
```

```json
{ "r": [{ "Label": "Lyon", "Items": [{ "nom": "Ana", "ville": "Lyon" }] }] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `group_paths` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
