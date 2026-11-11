<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isnotnull`

*Français · [English](isnotnull.en.md)*

Vrai si la valeur n'est ni null ni absente

```
isnotnull(token)
```

**Exemple**

```jslt
{ "presente": isnotnull($.a), "absente": isnotnull($.z) }
```

```json
{ "a": 0 }
```

```json
{ "presente": true, "absente": false }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Types, repli sur erreur et validation](../types.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
