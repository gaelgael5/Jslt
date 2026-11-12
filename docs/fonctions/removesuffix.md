<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `removesuffix`

*Français · [English](removesuffix.en.md)*

Retire un suffixe **entier** s'il est présent, sinon rend le texte inchangé

```
removesuffix(token, suffix)
```

**Exemple**

```jslt
{ "present": removesuffix($.t, ".json"), "absent": removesuffix($.t, ".xml") }
```

```json
{ "t": "contrat.json" }
```

```json
{ "present": "contrat", "absent": "contrat.json" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `suffix` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
