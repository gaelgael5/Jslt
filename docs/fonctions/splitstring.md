<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `splitstring`

*Français · [English](splitstring.en.md)*

Découpe un texte sur un séparateur complet (plusieurs caractères), au plus limit fois

```
splitstring(token, separator, limit)
```

**Exemples**

*Un séparateur **entier**, là où `split` ne garde que son 1er caractère.*

```jslt
{ "entier": splitstring($.t, " - "), "premier_caractere": split($.t, " - ") }
```

```json
{ "t": "a - b - c" }
```

```json
{ "entier": ["a", "b", "c"], "premier_caractere": ["a", "-", "b", "-", "c"] }
```

*`limit` compte les **coupes** : `1` rend deux éléments, le reste du texte étant gardé entier.*

```jslt
{ "une_coupe": splitstring($.t, ",", 1) }
```

```json
{ "t": "a,b,c" }
```

```json
{ "une_coupe": ["a", "b,c"] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `separator` | optionnel |  |
| `limit` | optionnel |  |

**À savoir**

- `limit` est le nombre de **coupes**, pas de morceaux : avec `1`, on obtient deux éléments et le reste du texte est gardé entier.

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
