<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `renamekeys`

*Français · [English](renamekeys.en.md)*

Renomme les clés d'un objet selon un mapping { ancien: nouveau }

```
renamekeys(token, mapping)
```

**Exemple**

```jslt
{ "r": renamekeys($.o, { "nom": "name" }) }
```

```json
{ "o": { "nom": "Ana", "ville": "Lyon" } }
```

```json
{ "r": { "name": "Ana", "ville": "Lyon" } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `mapping` | optionnel |  |

**Chapitre** : [Objets et structures profondes](../objets.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
