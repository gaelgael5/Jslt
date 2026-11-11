<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `parsejson`

*Français · [English](parsejson.en.md)*

Lit un texte JSON et rend la valeur correspondante (objet, tableau ou scalaire)

```
parsejson(token)
```

**Exemple**

```jslt
{ "r": select(parsejson($.t), $.ville) }
```

```json
{ "t": "{\"ville\": \"Lyon\"}" }
```

```json
{ "r": "Lyon" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Types, repli sur erreur et validation](../types.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
