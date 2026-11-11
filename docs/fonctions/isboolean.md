<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isboolean`

*Français · [English](isboolean.en.md)*

Vrai si la valeur est un booléen (true ou false)

```
isboolean(token)
```

**Exemple**

```jslt
{ "r": isboolean($.b), "nombre": isboolean($.n) }
```

```json
{ "b": false, "n": 0 }
```

```json
{ "r": true, "nombre": false }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Types, repli sur erreur et validation](../types.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
