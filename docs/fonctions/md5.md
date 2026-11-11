<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `md5`

*Français · [English](md5.en.md)*

Empreinte MD5 d'une valeur, en hexadécimal (identité, pas signature)

```
md5(token)
```

**Exemple**

```jslt
{ "r": md5($.t) }
```

```json
{ "t": "abc" }
```

```json
{ "r": "900150983cd24fb0d6963f7d28e17f72" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Encodage, empreintes et échappement](../encodage.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
