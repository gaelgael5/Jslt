<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `regexismatch`

*Français · [English](regexismatch.en.md)*

Vrai si le texte contient une correspondance du motif regex

```
regexismatch(token, pattern)
```

**Exemple**

```jslt
{ "r": regexismatch($.t, "^[A-Z]{2}[0-9]+$") }
```

```json
{ "t": "FR123" }
```

```json
{ "r": true }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `pattern` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
