<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `similarity`

*Français · [English](similarity.en.md)*

Proximité de deux textes entre 0 (tout diffère) et 1 (identiques)

```
similarity(left, right)
```

**Exemple**

```jslt
{ "r": round(similarity($.a, $.b), 2) }
```

```json
{ "a": "Durand", "b": "Durrand" }
```

```json
{ "r": 0.86 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `left` | optionnel |  |
| `right` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
