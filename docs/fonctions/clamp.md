<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `clamp`

*Français · [English](clamp.en.md)*

Ramène un nombre dans l'intervalle [lower, upper]

```
clamp(token, lower, upper)
```

**Exemple**

```jslt
{ "r": clamp($.n, 0, 100) }
```

```json
{ "n": 142 }
```

```json
{ "r": 100 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `lower` | optionnel |  |
| `upper` | optionnel |  |

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
