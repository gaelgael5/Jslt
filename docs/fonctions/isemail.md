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

**À savoir**

- Volontairement **pragmatique** : la RFC 5322 complète accepte des formes que personne n'utilise, et les accepter laisserait passer ce qu'un système en aval refusera.

**Chapitre** : [Qualité : refuser, observer, valider](../qualite.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
