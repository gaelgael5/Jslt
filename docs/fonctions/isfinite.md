<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isfinite`

*Français · [English](isfinite.en.md)*

Vrai si la valeur est un nombre fini (ni infini, ni NaN)

```
isfinite(token)
```

**Exemple**

```jslt
{ "nombre": isfinite($.n), "texte": isfinite($.t) }
```

```json
{ "n": 3, "t": "3" }
```

```json
{ "nombre": true, "texte": false }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
