<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `sum`

*Français · [English](sum.en.md)*

Somme des nombres d'un tableau (0 pour un tableau vide ou null)

```
sum(token)
```

**Exemple**

```jslt
{ "r": sum($.n) }
```

```json
{ "n": [1, 2, 3] }
```

```json
{ "r": 6 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
