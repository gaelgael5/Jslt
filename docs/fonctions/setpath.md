<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `setpath`

*Français · [English](setpath.en.md)*

Copie de l'objet avec une valeur posée au bout d'un chemin pointé (niveaux créés au besoin)

```
setpath(token, path, value, separator)
```

**Exemple**

```jslt
{ "r": setpath($.o, "client.ville", "Lyon") }
```

```json
{ "o": { "client": { "nom": "Ana" } } }
```

```json
{ "r": { "client": { "nom": "Ana", "ville": "Lyon" } } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `path` | optionnel |  |
| `value` | optionnel |  |
| `separator` | optionnel |  |

**Chapitre** : [Objets et structures profondes](../objets.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
