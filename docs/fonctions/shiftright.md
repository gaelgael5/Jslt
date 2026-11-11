<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `shiftright`

*Français · [English](shiftright.en.md)*

Décale les bits d'un entier vers la droite (divise par 2^bits)

```
shiftright(token, bits)
```

**Exemple**

```jslt
{ "r": shiftright($.n, 3) }
```

```json
{ "n": 64 }
```

```json
{ "r": 8 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `bits` | optionnel |  |

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
