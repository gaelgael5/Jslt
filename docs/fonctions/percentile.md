<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `percentile`

*Français · [English](percentile.en.md)*

Centile p (0 à 100) des nombres d'un tableau, par interpolation linéaire

```
percentile(token, p)
```

**Exemple**

```jslt
{ "p90": percentile($.n, 90) }
```

```json
{ "n": [1, 2, 3, 4, 5] }
```

```json
{ "p90": 4.6 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `p` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
