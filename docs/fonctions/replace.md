<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `replace`

*Français · [English](replace.en.md)*

Remplace toutes les occurrences de search par replacement

```
replace(token, search, replacement)
```

**Exemple**

```jslt
{ "r": replace($.t, "-", "/") }
```

```json
{ "t": "2026-11-11" }
```

```json
{ "r": "2026/11/11" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `search` | optionnel |  |
| `replacement` | optionnel |  |

**À savoir**

- Remplace **toutes** les occurrences, littéralement : aucun caractère n'a de sens particulier. Pour un motif, `regexreplace`.

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
