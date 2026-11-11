<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `urlencode`

*Français · [English](urlencode.en.md)*

Encode une valeur pour une URL (mode path pour conserver les barres obliques)

```
urlencode(token, mode)
```

**Exemple**

```jslt
{ "r": urlencode($.t) }
```

```json
{ "t": "café noir" }
```

```json
{ "r": "caf%C3%A9%20noir" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `mode` | optionnel |  |

**À savoir**

- Le mode `"path"` **conserve les barres obliques** : c'est celui d'un chemin d'URL. Par défaut, elles sont encodées (`%2F`), ce qu'exige un paramètre.

**Chapitre** : [Encodage, empreintes et échappement](../encodage.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
