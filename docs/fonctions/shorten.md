<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `shorten`

*Français · [English](shorten.en.md)*

Raccourcit un texte à length caractères au plus, suffixe compris (… par défaut)

```
shorten(token, length, suffix)
```

**Exemple**

```jslt
{ "r": shorten($.t, 12) }
```

```json
{ "t": "Facture annuelle 2026" }
```

```json
{ "r": "Facture…" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `length` | optionnel |  |
| `suffix` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
