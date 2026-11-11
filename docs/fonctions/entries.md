<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `entries`

*Français · [English](entries.en.md)*

Paires d'un objet en tableau de { key, value }, dans l'ordre du document

```
entries(token)
```

**Exemple**

```jslt
{ "r": entries($.o) }
```

```json
{ "o": { "a": 1, "b": 2 } }
```

```json
{ "r": [{ "key": "a", "value": 1 }, { "key": "b", "value": 2 }] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Objets et structures profondes](../objets.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
