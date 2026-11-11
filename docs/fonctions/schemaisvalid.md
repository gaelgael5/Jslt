<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `schemaisvalid`

*Français · [English](schemaisvalid.en.md)*

Vrai si le document respecte le JSON Schema donné (sous-ensemble géré)

```
schemaisvalid(fragment, schema_document)
```

**Exemple**

```jslt
{ "r": schemaisvalid($.o, $.s) }
```

```json
{ "o": { "age": 42 }, "s": { "type": "object", "properties": { "age": { "type": "integer" } } } }
```

```json
{ "r": true }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `fragment` | optionnel |  |
| `schema_document` | optionnel |  |

**Chapitre** : [Types, repli sur erreur et validation](../types.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
