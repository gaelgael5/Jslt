<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `flattenobject`

*Français · [English](flattenobject.en.md)*

Aplatit un objet en clés pointées (a.b.c), tableaux indexés par leur position

```
flattenobject(token, separator)
```

**Exemple**

```jslt
{ "r": flattenobject($.o) }
```

```json
{ "o": { "client": { "nom": "Ana" } } }
```

```json
{ "r": { "client.nom": "Ana" } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `separator` | optionnel |  |

**À savoir**

- Les tableaux sont indexés par leur **position** (`l.0`, `l.1`) : c'est le pont vers un CSV, qui n'a pas de profondeur.

**Chapitre** : [Objets et structures profondes](../objets.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
