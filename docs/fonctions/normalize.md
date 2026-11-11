<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `normalize`

*Français · [English](normalize.en.md)*

Normalise une chaîne Unicode : forme C (défaut), D, KC ou KD

```
normalize(token, form)
```

**Exemple**

```jslt
{ "r": stringlenght(normalize($.t, "C")) }
```

```json
{ "t": "é" }
```

```json
{ "r": 1 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `form` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
