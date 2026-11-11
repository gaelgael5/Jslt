<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `trydefault`

*Français · [English](trydefault.en.md)*

Valeur de l'expression, ou celle du repli si l'expression lève une erreur

```
trydefault(expression, fallback)
```

**Exemple**

```jslt
{ "r": trydefault($.a / $.b, "division impossible") }
```

```json
{ "a": 1, "b": 0 }
```

```json
{ "r": "division impossible" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `expression` | optionnel | expression **non évaluée**, calculée par la fonction |
| `fallback` | optionnel | expression **non évaluée**, calculée par la fonction |

**À savoir**

- Le repli n'est évalué **que** si la première expression lève : il peut donc être coûteux sans ralentir le cas nominal.
- Il n'attrape que les erreurs du moteur (`JsltError`), pas une valeur `null` : pour un repli sur l'absence, l'opérateur `??`.

**Chapitre** : [Types, repli sur erreur et validation](../types.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
