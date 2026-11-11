<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `keys`

*Français · [English](keys.en.md)*

Clés d'un objet, dans l'ordre du document (null si ce n'est pas un objet)

```
keys(token)
```

**Exemple**

```jslt
{ "r": keys($.o) }
```

```json
{ "o": { "a": 1, "b": 2 } }
```

```json
{ "r": ["a", "b"] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Objets et structures profondes](../objets.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
