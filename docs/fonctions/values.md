<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `values`

*Français · [English](values.en.md)*

Valeurs d'un objet, dans l'ordre du document (null si ce n'est pas un objet)

```
values(token)
```

**Exemple**

```jslt
{ "r": values($.o) }
```

```json
{ "o": { "a": 1, "b": 2 } }
```

```json
{ "r": [1, 2] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Objets et structures profondes](../objets.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
