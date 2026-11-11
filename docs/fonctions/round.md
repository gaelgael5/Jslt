<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `round`

*Français · [English](round.en.md)*

Arrondi à l'entier le plus proche, demi vers le pair (2.5 -> 2.0, 3.5 -> 4.0), rendu en décimal

```
round(token, digits)
```

**Exemple**

```jslt
{ "pair": round($.a), "deux_decimales": round($.b, 2) }
```

```json
{ "a": 2.5, "b": 1.2345 }
```

```json
{ "pair": 2.0, "deux_decimales": 1.23 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `digits` | optionnel |  |

**À savoir**

- Arrondi **bancaire** (au pair le plus proche) : `2.5` donne `2` et `3.5` donne `4`. Pour couper vers zéro, `truncate` ; vers le haut, `ceil`.

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
