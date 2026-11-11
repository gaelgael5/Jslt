<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `chars`

*Français · [English](chars.en.md)*

Découpe un texte en tableau de caractères (par graphème)

```
chars(token)
```

**Exemple**

*Par **graphème** : un « e » suivi d'un accent combinant reste un caractère.*

```jslt
{ "r": chars($.t) }
```

```json
{ "t": "été" }
```

```json
{ "r": ["é", "t", "é"] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Texte, expressions régulières et formatage](../texte.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
