<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `requirethat`

*Français · [English](requirethat.en.md)*

Vérifie une condition et lève avec le message donné si elle n'est pas vraie

```
requirethat(condition, message)
```

**Exemple**

```jslt
{ "r": trydefault(requirethat($.n > 100, "montant trop faible"), "refusé") }
```

```json
{ "n": 10 }
```

```json
{ "r": "refusé" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `condition` | optionnel |  |
| `message` | optionnel |  |

**À savoir**

- Exige `true` **strict** : une condition qui vaut `0` ou `""` est refusée, parce que c'est presque toujours une expression qu'on croyait booléenne.

**Chapitre** : [Qualité : refuser, observer, valider](../qualite.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
