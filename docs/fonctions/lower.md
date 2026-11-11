<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `lower`

*Français · [English](lower.en.md)*

Texte en minuscules (null reste null, une non-chaîne donne false)

```
lower(token)
```

**Exemple**

```jslt
{ "r": lower($.t) }
```

```json
{ "t": "ACME SA" }
```

```json
{ "r": "acme sa" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
