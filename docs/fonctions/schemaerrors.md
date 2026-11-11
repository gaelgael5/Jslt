<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `schemaerrors`

*Français · [English](schemaerrors.en.md)*

Liste des erreurs de validation d'un document contre un JSON Schema (vide si conforme)

```
schemaerrors(fragment, schema_document)
```

**Exemple**

```jslt
{ "r": schemaerrors($.o, $.s) }
```

```json
{ "o": { "age": "vieux" }, "s": { "type": "object", "properties": { "age": { "type": "integer" } } } }
```

```json
{ "r": ["$.age : attendu un entier, reçu une chaîne"] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `fragment` | optionnel |  |
| `schema_document` | optionnel |  |

**Chapitre** : [Types, repli sur erreur et validation](../types.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
