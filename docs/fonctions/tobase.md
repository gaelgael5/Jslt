<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `tobase`

*Français · [English](tobase.en.md)*

Écrit un entier dans une base de 2 à 36, complété à width chiffres

```
tobase(token, base, width)
```

**Exemple**

```jslt
{ "binaire": tobase($.n, 2), "sur_huit": tobase($.n, 2, 8) }
```

```json
{ "n": 11 }
```

```json
{ "binaire": "1011", "sur_huit": "00001011" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `base` | optionnel |  |
| `width` | optionnel |  |

**À savoir**

- Bases de 2 à 36 (chiffres puis lettres minuscules). `width` complète de zéros à gauche ; le signe est écrit **devant** les chiffres, un entier JSON n'ayant pas de largeur fixe.

**Chapitre** : [Nombres et maths](../nombres.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
