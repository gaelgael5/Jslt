<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `trim`

*Français · [English](trim.en.md)*

Retire les espaces en début et fin, ou les caractères de txt s'il est donné

```
trim(token, txt)
```

**Exemple**

```jslt
{ "espaces": trim($.a), "caracteres": trim($.b, "*") }
```

```json
{ "a": "  ok  ", "b": "**ok**" }
```

```json
{ "espaces": "ok", "caracteres": "ok" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `txt` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
