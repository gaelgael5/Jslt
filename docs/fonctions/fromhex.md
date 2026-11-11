<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `fromhex`

*Français · [English](fromhex.en.md)*

Lit un entier écrit en hexadécimal (avec ou sans préfixe 0x)

```
fromhex(token)
```

**Exemple**

```jslt
{ "r": fromhex($.t) }
```

```json
{ "t": "0xff" }
```

```json
{ "r": 255 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
