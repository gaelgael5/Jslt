<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `trace`

*Français · [English](trace.en.md)*

Rend la valeur inchangée et l'enregistre dans le journal, lisible par traces()

```
trace(value, label)
```

**Exemple**

```jslt
{ "r": trace($.n, "montant") }
```

```json
{ "n": 42 }
```

```json
{ "r": 42 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `value` | optionnel |  |
| `label` | optionnel |  |

**À savoir**

- Le journal vit sur le **contexte d'exécution** : deux exécutions concurrentes ne se mélangent pas, et un intégrateur le lit après coup (`context.traces`) sans que le template ait à le recopier dans sa sortie.

**Chapitre** : [Qualité : refuser, observer, valider](../qualite.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
