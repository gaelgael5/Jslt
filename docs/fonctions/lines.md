<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `lines`

*Français · [English](lines.en.md)*

Découpe un texte en lignes (\n, \r\n ou \r), lignes vides comprises

```
lines(token)
```

**Exemple**

*Les trois fins de ligne, et les lignes **vides** sont gardées.*

```jslt
{ "r": lines($.t) }
```

```json
{ "t": "a\nb\n\nc" }
```

```json
{ "r": ["a", "b", "", "c"] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
