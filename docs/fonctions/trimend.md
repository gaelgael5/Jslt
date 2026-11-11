<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `trimend`

*Français · [English](trimend.en.md)*

Retire les espaces en fin, ou les caractères de txt

```
trimend(token, txt)
```

**Exemple**

```jslt
{ "r": trimend($.t) }
```

```json
{ "t": "ok   " }
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
