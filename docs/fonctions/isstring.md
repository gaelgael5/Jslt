<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isstring`

*Français · [English](isstring.en.md)*

Vrai si la valeur est une chaîne de caractères

```
isstring(token)
```

**Exemple**

```jslt
{ "texte": isstring($.t), "nombre": isstring($.n) }
```

```json
{ "t": "a", "n": 1 }
```

```json
{ "texte": true, "nombre": false }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Types, repli sur erreur et validation](../types.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
