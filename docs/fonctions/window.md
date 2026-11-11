<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `window`

*Français · [English](window.en.md)*

Fenêtres glissantes de size éléments consécutifs (vide si le tableau est plus court)

```
window(source, size)
```

**Exemple**

```jslt
{ "r": window($.l, 2) }
```

```json
{ "l": [1, 2, 3] }
```

```json
{ "r": [[1, 2], [2, 3]] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `size` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
