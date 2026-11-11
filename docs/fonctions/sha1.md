<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `sha1`

*Français · [English](sha1.en.md)*

Empreinte SHA-1 d'une valeur, en hexadécimal (identité, pas signature)

```
sha1(token)
```

**Exemple**

```jslt
{ "r": sha1($.t) }
```

```json
{ "t": "abc" }
```

```json
{ "r": "a9993e364706816aba3e25717850c26c9cd0d89d" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Encodage, empreintes et échappement](../encodage.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
