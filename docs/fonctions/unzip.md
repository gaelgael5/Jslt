<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `unzip`

*Français · [English](unzip.en.md)*

Inverse de zip : d'un tableau de rangées, rend un tableau par position

```
unzip(source)
```

**Exemple**

```jslt
{ "r": unzip($.l) }
```

```json
{ "l": [[1, "a"], [2, "b"]] }
```

```json
{ "r": [[1, 2], ["a", "b"]] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
