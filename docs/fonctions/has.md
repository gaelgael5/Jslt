<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `has`

*Français · [English](has.en.md)*

Vrai si l'objet porte cette clé, même avec une valeur nulle

```
has(token, key)
```

**Exemple**

```jslt
{ "presente": has($.o, "a"), "absente": has($.o, "z") }
```

```json
{ "o": { "a": null } }
```

```json
{ "presente": true, "absente": false }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `key` | optionnel |  |

**Chapitre** : [Objets et structures profondes](../objets.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
