<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `regexreplace`

*Français · [English](regexreplace.en.md)*

Remplace les correspondances d'un motif regex ($1, ${nom}, $& pour les groupes)

```
regexreplace(token, pattern, replacement)
```

**Exemple**

```jslt
{ "r": regexreplace($.t, "(\\d{4})-(\\d{2})", "$2/$1") }
```

```json
{ "t": "2026-11" }
```

```json
{ "r": "11/2026" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `pattern` | optionnel |  |
| `replacement` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
