<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `splitregex`

*Français · [English](splitregex.en.md)*

Découpe un texte sur les correspondances d'un motif regex

```
splitregex(token, pattern, limit)
```

**Exemple**

```jslt
{ "r": splitregex($.t, "\\s*;\\s*") }
```

```json
{ "t": "a ; b;c" }
```

```json
{ "r": ["a", "b", "c"] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `pattern` | optionnel |  |
| `limit` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
