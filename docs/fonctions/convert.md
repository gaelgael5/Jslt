<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `convert`

*Français · [English](convert.en.md)*

Convertit une valeur vers un type : integer, decimal, string, boolean (uri, uuid, datetime, time en texte)

```
convert(token, target_type)
```

**Exemple**

```jslt
{ "entier": convert($.t, "integer"), "texte": convert($.n, "string") }
```

```json
{ "t": "42", "n": 7 }
```

```json
{ "entier": 42, "texte": "7" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `target_type` | optionnel |  |

**À savoir**

- Types : `integer`, `decimal`, `string`, `boolean` — complets ; `uri`, `uuid`, `datetime`, `time` sont rendus **en texte** (le portage n'a pas ces types). La forme `$.x #integer` fait la même chose.

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
