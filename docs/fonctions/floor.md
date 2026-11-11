<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `floor`

*Français · [English](floor.en.md)*

Arrondi vers le bas, à l'entier (2.7 -> 2.0) ou à digits décimales

```
floor(token, digits)
```

**Exemple**

```jslt
{ "entier": floor($.n), "deux_decimales": floor($.n, 2) }
```

```json
{ "n": 2.349 }
```

```json
{ "entier": 2.0, "deux_decimales": 2.34 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `digits` | optionnel |  |

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
