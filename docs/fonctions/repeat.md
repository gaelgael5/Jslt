<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `repeat`

*Français · [English](repeat.en.md)*

Répète le texte count fois (0 ou négatif : chaîne vide)

```
repeat(token, count)
```

**Exemple**

```jslt
{ "r": repeat($.t, 3) }
```

```json
{ "t": "ab" }
```

```json
{ "r": "ababab" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `count` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
