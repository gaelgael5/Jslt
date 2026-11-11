<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `parsenumber`

*Français · [English](parsenumber.en.md)*

Lit un nombre écrit en texte selon une culture (1 234,56 en fr-FR)

```
parsenumber(token, culture)
```

**Exemple**

```jslt
{ "r": parsenumber($.t, "fr-FR") }
```

```json
{ "t": "1 234,56" }
```

```json
{ "r": 1234.56 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `culture` | optionnel |  |

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
