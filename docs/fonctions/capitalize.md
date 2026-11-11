<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `capitalize`

*Français · [English](capitalize.en.md)*

Met en majuscule la première lettre seulement, sans toucher au reste

```
capitalize(token)
```

**Exemple**

*La première lettre **seulement** ; `titlecase` met toutes les initiales.*

```jslt
{ "cap": capitalize($.t), "titre": titlecase($.t) }
```

```json
{ "t": "bonjour le MONDE" }
```

```json
{ "cap": "Bonjour le MONDE", "titre": "Bonjour Le MONDE" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
