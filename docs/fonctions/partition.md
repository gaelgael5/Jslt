<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `partition`

*Français · [English](partition.en.md)*

Sépare un tableau en { true, false } selon un prédicat évalué par élément

```
partition(source, predicate)
```

**Exemple**

```jslt
{ "r": partition($.l, $.actif) }
```

```json
{ "l": [{ "n": "a", "actif": true }, { "n": "b", "actif": false }] }
```

```json
{ "r": { "true": [{ "n": "a", "actif": true }], "false": [{ "n": "b", "actif": false }] } }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source` | optionnel |  |
| `predicate` | optionnel | expression **non évaluée**, calculée par la fonction |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
