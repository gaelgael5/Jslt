<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `words`

*Français · [English](words.en.md)*

Découpe un texte en mots sur les espaces (les vides sont ignorés)

```
words(token)
```

**Exemple**

```jslt
{ "r": words($.t) }
```

```json
{ "t": "  le   petit chat " }
```

```json
{ "r": ["le", "petit", "chat"] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
