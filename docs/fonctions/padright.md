<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `padright`

*Français · [English](padright.en.md)*

Complète le texte à droite jusqu'à length avec le 1er caractère de charset (espace par défaut)

```
padright(token, length, charset)
```

**Exemple**

```jslt
{ "r": padright($.t, 6, ".") }
```

```json
{ "t": "42" }
```

```json
{ "r": "42...." }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `length` | optionnel |  |
| `charset` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
