<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `indexof`

*Français · [English](indexof.en.md)*

Position (à partir de 0) de la première occurrence dans un texte ou un tableau, -1 si absent

```
indexof(token, txt)
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

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
