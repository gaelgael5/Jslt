<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `split`

*Français · [English](split.en.md)*

Découpe un texte en tableau sur le premier caractère de charset (séparateur entier : splitstring)

```
split(token, charset)
```

**Exemple**

```jslt
{ "r": split($.t, ";") }
```

```json
{ "t": "a;b;c" }
```

```json
{ "r": ["a", "b", "c"] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `charset` | optionnel |  |

**À savoir**

- Seul le **premier caractère** du séparateur est retenu : `split($.t, ", ")` coupe sur la virgule et laisse les espaces. Pour un séparateur entier, `splitstring`.

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
