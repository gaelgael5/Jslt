<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `ceil`

*Français · [English](ceil.en.md)*

Arrondi vers le haut, à l'entier (2.1 -> 3.0) ou à digits décimales

```
ceil(token, digits)
```

**Exemple**

```jslt
{ "entier": ceil($.n), "deux_decimales": ceil($.n, 2) }
```

```json
{ "n": 2.341 }
```

```json
{ "entier": 3.0, "deux_decimales": 2.35 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `digits` | optionnel |  |

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
