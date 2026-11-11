<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `startswith`

*Français · [English](startswith.en.md)*

Vrai si le texte commence par txt

```
startswith(token, txt)
```

**Exemple**

```jslt
{ "r": startswith($.t, "FR") }
```

```json
{ "t": "FR7630006000011234567890189" }
```

```json
{ "r": true }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `txt` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
