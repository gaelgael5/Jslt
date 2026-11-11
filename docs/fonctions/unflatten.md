<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `unflatten`

*Français · [English](unflatten.en.md)*

Reconstruit un objet imbriqué depuis des clés pointées (arrays à true pour les indices)

```
unflatten(token, separator, arrays)
```

**Exemple**

```jslt
{ "r": unflatten($.o) }
```

```json
{ "o": { "client.nom": "Ana" } }
```

```json
{ "r": { "client": { "nom": "Ana" } } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `separator` | optionnel |  |
| `arrays` | optionnel |  |

**Chapitre** : [Objets et structures profondes](../objets.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
