<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `regexmatches`

*Français · [English](regexmatches.en.md)*

Liste des correspondances du motif regex dans le texte

```
regexmatches(token, pattern)
```

**Exemple**

```jslt
{ "r": regexmatches($.t, "[0-9]+") }
```

```json
{ "t": "a1 b22 c333" }
```

```json
{ "r": ["1", "22", "333"] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `pattern` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
