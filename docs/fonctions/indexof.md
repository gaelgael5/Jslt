<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `indexof`

*Français · [English](indexof.en.md)*

Position (à partir de 0) de la première occurrence dans un texte ou un tableau, -1 si absent ; start cherche à partir de cette position

```
indexof(token, txt, start)
```

**Exemple**

```jslt
{ "texte": indexof($.t, "o"), "tableau": indexof($.l, "b") }
```

```json
{ "t": "bonjour", "l": ["a", "b", "c"] }
```

```json
{ "texte": 1, "tableau": 1 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `txt` | optionnel |  |
| `start` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
