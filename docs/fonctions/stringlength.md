<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `stringlength`

*Français · [English](stringlength.en.md)*

Nombre de caractères d'un texte (0 pour null ou une non-chaîne)

```
stringlength(token)
```

**Exemple**

*Même fonction que `stringlenght`, dont l'orthographe d'origine est fautive.*

```jslt
{ "r": stringlength($.t) }
```

```json
{ "t": "Ana" }
```

```json
{ "r": 3 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**À savoir**

- Même fonction que `stringlenght`, dont l'orthographe d'origine est fautive : les deux noms enregistrent la **même** implémentation, donc ils ne peuvent pas diverger. Retirer l'ancien casserait les templates écrits avec.

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
