<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `require`

*Français · [English](require.en.md)*

Rend la valeur si elle est présente, sinon lève avec le message donné

```
require(value, message)
```

**Exemple**

```jslt
{ "r": require($.n, "le montant est obligatoire") }
```

```json
{ "n": 0 }
```

```json
{ "r": 0 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `value` | optionnel |  |
| `message` | optionnel |  |

**Chapitre** : [Qualité : refuser, observer, valider](../qualite.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
