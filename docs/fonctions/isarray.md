<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isarray`

*Français · [English](isarray.en.md)*

Vrai si la valeur est un tableau JSON

```
isarray(token)
```

**Exemple**

```jslt
{ "tableau": isarray($.l), "objet": isarray($.o) }
```

```json
{ "l": [], "o": {} }
```

```json
{ "tableau": true, "objet": false }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Types, repli sur erreur et validation](../types.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
