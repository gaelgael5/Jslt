<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `roundhalfup`

*Français · [English](roundhalfup.en.md)*

Arrondi commercial : les demis s'éloignent de zéro (0.125 -> 0.13), à l'entier ou à digits décimales

```
roundhalfup(token, digits)
```

**Exemple**

*`round($.n, 2)` rendrait `0.12` : il arrondit le demi vers le **pair**.*

```jslt
{ "commercial": roundhalfup($.n, 2), "bancaire": round($.n, 2) }
```

```json
{ "n": 0.125 }
```

```json
{ "commercial": 0.13, "bancaire": 0.12 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `digits` | optionnel | nombre de décimales ; absent, arrondi à l'entier ; négatif, aux dizaines (`-2` = à la centaine) |

**À savoir**

- L'arrondi **commercial**, là où `round` est bancaire : `round(0.125, 2)` rend `0.12`. Les demis **s'éloignent de zéro**, donc `-0.5` rend `-1` — un avoir s'arrondit comme la facture qu'il annule.
- Le nombre est lu tel qu'il est **écrit** : `2.675` se stocke en `2.67499999…`, et un arrondi conduit sur cette valeur rendrait `2.67`.

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
