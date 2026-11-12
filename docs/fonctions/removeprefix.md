<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `removeprefix`

*Français · [English](removeprefix.en.md)*

Retire un préfixe **entier** s'il est présent, sinon rend le texte inchangé

```
removeprefix(token, prefix)
```

**Exemple**

*Un **affixe entier**, là où `trimstart` retire un jeu de caractères : sur « bacab », `trimstart($.t, "ab")` rend « cab » alors que le préfixe n'y est pas.*

```jslt
{ "present": removeprefix($.t, "ba"), "absent": removeprefix($.t, "ab"), "jeu": trimstart($.t, "ab") }
```

```json
{ "t": "bacab" }
```

```json
{ "present": "cab", "absent": "bacab", "jeu": "cab" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `prefix` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
