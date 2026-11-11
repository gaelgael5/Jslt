<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `avg`

*Français · [English](avg.en.md)*

Moyenne des nombres d'un tableau (null pour un tableau vide)

```
avg(token)
```

**Exemple**

```jslt
{ "r": avg($.n) }
```

```json
{ "n": [1, 2, 6] }
```

```json
{ "r": 3.0 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
