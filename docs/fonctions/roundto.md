<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `roundto`

*Français · [English](roundto.en.md)*

Arrondi au multiple le plus proche (roundto(2.34, 0.05) -> 2.35), demi en s'éloignant de zéro

```
roundto(token, step)
```

**Exemple**

```jslt
{ "caisse": roundto($.n, 0.05), "quart_heure": roundto($.m, 15) }
```

```json
{ "n": 2.34, "m": 38 }
```

```json
{ "caisse": 2.35, "quart_heure": 45.0 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `step` | optionnel | le pas d'arrondi, strictement positif (`0.05`, `15`, `0.25`) ; nul ou négatif, il lève |

**À savoir**

- Un pas nul ou négatif **lève**, plutôt que de rendre une valeur qui n'a été arrondie à rien — ce qu'un `roundto($.n, $.pas)` au pas absent produirait.
- Les demis s'éloignent de zéro, comme `roundhalfup`, et le calcul ne passe pas par un flottant intermédiaire : le contournement `round($.n * 20) / 20` le faisait, avec l'erreur de représentation qui va avec.

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
