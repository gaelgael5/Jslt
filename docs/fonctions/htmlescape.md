<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `htmlescape`

*Français · [English](htmlescape.en.md)*

Échappe les caractères qui ont un sens en HTML (< > & " ')

```
htmlescape(token)
```

**Exemple**

```jslt
{ "r": htmlescape($.t) }
```

```json
{ "t": "<b>ok</b>" }
```

```json
{ "r": "&lt;b&gt;ok&lt;/b&gt;" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Encodage, empreintes et échappement](../encodage.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
