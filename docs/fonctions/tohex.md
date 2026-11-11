<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `tohex`

*Français · [English](tohex.en.md)*

Écrit un entier en hexadécimal minuscule, complété à width chiffres

```
tohex(token, width)
```

**Exemple**

```jslt
{ "r": tohex($.n), "sur_quatre": tohex($.n, 4) }
```

```json
{ "n": 255 }
```

```json
{ "r": "ff", "sur_quatre": "00ff" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `width` | optionnel |  |

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
