<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `lastindexof`

*Français · [English](lastindexof.en.md)*

Position (à partir de 0) de la dernière occurrence dans un texte ou un tableau, -1 si absent

```
lastindexof(token, txt)
```

**Exemple**

```jslt
{ "r": lastindexof($.t, "o") }
```

```json
{ "t": "bonjour" }
```

```json
{ "r": 4 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `txt` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
