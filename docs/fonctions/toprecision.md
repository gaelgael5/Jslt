<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `toprecision`

*Français · [English](toprecision.en.md)*

Arrondi à un nombre de chiffres significatifs (toprecision(1234.5, 3) -> 1230)

```
toprecision(token, digits)
```

**Exemple**

*Trois chiffres significatifs, quel que soit l'ordre de grandeur.*

```jslt
{ "grand": toprecision($.a, 3), "petit": toprecision($.b, 3) }
```

```json
{ "a": 1234.5, "b": 0.00241348 }
```

```json
{ "grand": 1230.0, "petit": 0.00241 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `digits` | optionnel | nombre de chiffres **significatifs**, au moins 1 (et non un nombre de décimales) |

**À savoir**

- Chiffres **significatifs**, pas décimales : `round($.n, 2)` fixe le rang de la virgule, ce qui n'a pas de sens sur une colonne où voisinent `0.00241` et `24100`.
- Moins d'un chiffre **lève** ; `0` est rendu tel quel, un zéro ayant autant de chiffres significatifs qu'on veut.

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
