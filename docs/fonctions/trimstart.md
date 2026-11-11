<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `trimstart`

*Français · [English](trimstart.en.md)*

Retire les espaces en début, ou les caractères de txt

```
trimstart(token, txt)
```

**Exemple**

```jslt
{ "r": trimstart($.t) }
```

```json
{ "t": "   ok" }
```

```json
{ "r": "ok" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `txt` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
