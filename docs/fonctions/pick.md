<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `pick`

*Français · [English](pick.en.md)*

Sous-objet limité aux clés demandées (une clé ou un tableau de clés)

```
pick(token, keys)
```

**Exemple**

```jslt
{ "r": pick($.o, ["nom", "ville"]) }
```

```json
{ "o": { "nom": "Ana", "ville": "Lyon", "secret": "x" } }
```

```json
{ "r": { "nom": "Ana", "ville": "Lyon" } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `keys` | optionnel |  |

**Chapitre** : [Objets et structures profondes](../objets.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
