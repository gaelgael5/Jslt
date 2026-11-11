<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `unsetpath`

*Français · [English](unsetpath.en.md)*

Copie de l'objet privée du chemin pointé (sans erreur s'il est absent)

```
unsetpath(token, path, separator)
```

**Exemple**

```jslt
{ "r": unsetpath($.o, "client.secret") }
```

```json
{ "o": { "client": { "nom": "Ana", "secret": "x" } } }
```

```json
{ "r": { "client": { "nom": "Ana" } } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `path` | optionnel |  |
| `separator` | optionnel |  |

**À savoir**

- Rend une copie ; un chemin absent n'est **pas** une erreur.

**Chapitre** : [Objets et structures profondes](../objets.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
