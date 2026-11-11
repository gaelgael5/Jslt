<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `frombase64`

*Français · [English](frombase64.en.md)*

Décode un texte Base64 en texte UTF-8

```
frombase64(token)
```

**Exemple**

```jslt
{ "r": frombase64($.t) }
```

```json
{ "t": "Ym9uam91cg==" }
```

```json
{ "r": "bonjour" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Encodage, empreintes et échappement](../encodage.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
