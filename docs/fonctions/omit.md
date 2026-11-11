<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `omit`

*Français · [English](omit.en.md)*

Objet privé des clés demandées (une clé ou un tableau de clés)

```
omit(token, keys)
```

**Exemple**

```jslt
{ "r": omit($.o, ["secret"]) }
```

```json
{ "o": { "nom": "Ana", "secret": "x" } }
```

```json
{ "r": { "nom": "Ana" } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `keys` | optionnel |  |

**Chapitre** : [Objets et structures profondes](../objets.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
