<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `append`

*Français · [English](append.en.md)*

Copie du tableau avec une valeur ajoutée à la fin

```
append(source, value)
```

**Exemple**

*Ajoute **une** valeur ; un tableau ajouté devient un élément imbriqué.*

```jslt
{ "valeur": append($.l, 3), "tableau": append($.l, [3, 4]), "source": $.l }
```

```json
{ "l": [1, 2] }
```

```json
{ "valeur": [1, 2, 3], "tableau": [1, 2, [3, 4]], "source": [1, 2] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `value` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
