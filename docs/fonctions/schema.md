<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `schema`

*Français · [English](schema.en.md)*

JSON Schema (draft-04) déduit d'un fragment JSON d'exemple

```
schema(fragment)
```

**Exemple**

```jslt
{ "r": schema($.o) }
```

```json
{ "o": { "nom": "Ana" } }
```

```json
{ "r": { "$schema": "http://json-schema.org/draft-04/schema#", "type": "object", "properties": { "nom": { "type": "string" } } } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `fragment` | optionnel |  |

**Chapitre** : [Types, repli sur erreur et validation](../types.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
