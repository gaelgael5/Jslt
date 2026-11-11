<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isurl`

*Français · [English](isurl.en.md)*

Vrai si le texte a la forme d'une URL avec son schéma

```
isurl(token)
```

**Exemple**

```jslt
{ "r": isurl($.t) }
```

```json
{ "t": "https://exemple.fr/a" }
```

```json
{ "r": true }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Qualité : refuser, observer, valider](../qualite.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
