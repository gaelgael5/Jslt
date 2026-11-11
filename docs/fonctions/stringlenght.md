<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `stringlenght`

*Français · [English](stringlenght.en.md)*

Nombre de caractères d'un texte (0 pour null ou une non-chaîne) — orthographe d'origine conservée

```
stringlenght(token)
```

**Exemple**

```jslt
{ "r": stringlenght($.t) }
```

```json
{ "t": "bonjour" }
```

```json
{ "r": 7 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
