<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `variance`

*Français · [English](variance.en.md)*

Variance des nombres d'un tableau : de population par défaut, d'échantillon si sample vaut true

```
variance(token, sample)
```

**Exemple**

```jslt
{ "r": variance($.n) }
```

```json
{ "n": [2, 4, 4, 4, 5, 5, 7, 9] }
```

```json
{ "r": 4.0 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `sample` | optionnel |  |

**À savoir**

- De **population** par défaut : les données d'un template sont l'ensemble, pas un tirage. `sample` à `true` applique la correction de Bessel (n−1).

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
