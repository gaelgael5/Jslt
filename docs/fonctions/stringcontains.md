<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `stringcontains`

*Français · [English](stringcontains.en.md)*

Vrai si le texte contient contain_str

```
stringcontains(token, contain_str)
```

**Exemple**

```jslt
{ "r": stringcontains($.t, "@") }
```

```json
{ "t": "ana@exemple.fr" }
```

```json
{ "r": true }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `contain_str` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
