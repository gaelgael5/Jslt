<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `sign`

*Français · [English](sign.en.md)*

Signe d'un nombre : -1, 0 ou 1

```
sign(token)
```

**Exemple**

```jslt
{ "negatif": sign($.a), "zero": sign($.b), "positif": sign($.c) }
```

```json
{ "a": -4, "b": 0, "c": 7 }
```

```json
{ "negatif": -1, "zero": 0, "positif": 1 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
