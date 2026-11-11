<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `traces`

*Français · [English](traces.en.md)*

Journal des valeurs observées par trace() dans cette exécution

```
traces()
```

**Exemple**

```jslt
{ "r": trace($.n, "montant"), "journal": traces() }
```

```json
{ "n": 42 }
```

```json
{ "r": 42, "journal": [{ "label": "montant", "value": 42 }] }
```

Cette fonction ne prend aucun argument.

**Chapitre** : [Qualité : refuser, observer, valider](../qualite.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
