<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `atan2`

*Français · [English](atan2.en.md)*

Angle en radians du point (x = right, y = left) : atan2(y, x)

```
atan2(left, right)
```

**Exemple**

```jslt
{ "r": atan2($.y, $.x) }
```

```json
{ "y": 0, "x": 1 }
```

```json
{ "r": 0.0 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `left` | optionnel |  |
| `right` | optionnel |  |

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
