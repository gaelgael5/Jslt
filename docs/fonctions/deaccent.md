<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `deaccent`

*Français · [English](deaccent.en.md)*

Retire les diacritiques (accents, cédilles) sans toucher à la casse

```
deaccent(token)
```

**Exemple**

```jslt
{ "r": deaccent($.t) }
```

```json
{ "t": "Évêché" }
```

```json
{ "r": "Eveche" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
