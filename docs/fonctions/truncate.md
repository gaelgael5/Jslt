<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `truncate`

*Français · [English](truncate.en.md)*

Coupe vers zéro (-2.7 -> -2.0), à l'entier ou à digits décimales

```
truncate(token, digits)
```

**Exemple**

```jslt
{ "vers_zero": truncate($.n), "deux_decimales": truncate($.n, 2) }
```

```json
{ "n": -2.789 }
```

```json
{ "vers_zero": -2.0, "deux_decimales": -2.78 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `digits` | optionnel |  |

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
