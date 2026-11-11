<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `prune`

*Français · [English](prune.en.md)*

Retire récursivement les null d'une structure, et le vide avec l'option empty

```
prune(token, options)
```

**Exemple**

```jslt
{ "nulls": prune($.o), "vides_aussi": prune($.o, "empty") }
```

```json
{ "o": { "a": 1, "b": null, "c": "" } }
```

```json
{ "nulls": { "a": 1, "c": "" }, "vides_aussi": { "a": 1 } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `options` | optionnel |  |

**Chapitre** : [Objets et structures profondes](../objets.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
