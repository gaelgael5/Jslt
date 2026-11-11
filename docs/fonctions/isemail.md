<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isemail`

*Français · [English](isemail.en.md)*

Vrai si le texte a la forme d'une adresse électronique

```
isemail(token)
```

**Exemple**

```jslt
{ "r": isemail($.t) }
```

```json
{ "t": "ana@exemple.fr" }
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
