<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `tobase64`

*Français · [English](tobase64.en.md)*

Encode une valeur en Base64 (texte UTF-8 ; objet ou tableau sérialisé en JSON)

```
tobase64(token)
```

**Exemple**

```jslt
{ "r": tobase64($.t) }
```

```json
{ "t": "bonjour" }
```

```json
{ "r": "Ym9uam91cg==" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Encodage, empreintes et échappement](../encodage.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
