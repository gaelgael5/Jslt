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

**À savoir**

- Le remplacement s'écrit avec `$` : `$1` (groupe numéroté), `${nom}` (groupe nommé), `$&` (toute la correspondance), `$$` (un `$` littéral).
- Comme les autres regex, un scalaire est **converti en texte** (`42` devient `"42"`), là où `replace` rendrait `false`.

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
