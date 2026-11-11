<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `htmlunescape`

*Français · [English](htmlunescape.en.md)*

Remplace les entités HTML (&amp;, &lt;…) par leurs caractères

```
htmlunescape(token)
```

**Exemple**

```jslt
{ "r": htmlunescape($.t) }
```

```json
{ "t": "&lt;b&gt;ok&lt;/b&gt;" }
```

```json
{ "r": "<b>ok</b>" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Encodage, empreintes et échappement](../encodage.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
