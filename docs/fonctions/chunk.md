<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `chunk`

*Français · [English](chunk.en.md)*

Découpe un tableau en tranches consécutives de size éléments

```
chunk(source, size)
```

**Exemple**

```jslt
{ "r": chunk($.l, 2) }
```

```json
{ "l": [1, 2, 3, 4, 5] }
```

```json
{ "r": [[1, 2], [3, 4], [5]] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `size` | optionnel |  |

**À savoir**

- Une taille nulle ou négative **lève** : c'est une faute d'écriture, pas une donnée surprenante.

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
