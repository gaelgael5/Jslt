<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `substring`

*Français · [English](substring.en.md)*

Extrait length caractères à partir de start (start négatif = depuis la fin, length absente = jusqu'au bout)

```
substring(token, start, length)
```

**Exemple**

```jslt
{ "debut": substring($.t, 0, 3), "depuis_la_fin": substring($.t, -2) }
```

```json
{ "t": "bonjour" }
```

```json
{ "debut": "bon", "depuis_la_fin": "ur" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `start` | optionnel |  |
| `length` | optionnel |  |

**À savoir**

- Des bornes trop larges ne **lèvent pas** : un début hors du texte rend une chaîne vide, une longueur trop grande s'arrête à la fin. Un template transforme des données qu'il ne choisit pas.
- Une longueur **négative** lève, elle : c'est une faute d'écriture.

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
