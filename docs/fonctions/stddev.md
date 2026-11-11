<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `stddev`

*Français · [English](stddev.en.md)*

Écart-type des nombres d'un tableau : de population par défaut, d'échantillon si sample vaut true

```
stddev(token, sample)
```

**Exemple**

```jslt
{ "population": stddev($.n), "echantillon": round(stddev($.n, true), 3) }
```

```json
{ "n": [2, 4, 4, 4, 5, 5, 7, 9] }
```

```json
{ "population": 2.0, "echantillon": 2.138 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `sample` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
