<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isnumber`

*Français · [English](isnumber.en.md)*

Vrai si la valeur est un nombre (un booléen n'en est pas un)

```
isnumber(token)
```

**Exemple**

```jslt
{ "nombre": isnumber($.n), "booleen": isnumber($.b) }
```

```json
{ "n": 3, "b": true }
```

```json
{ "nombre": true, "booleen": false }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Types, repli sur erreur et validation](../types.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
