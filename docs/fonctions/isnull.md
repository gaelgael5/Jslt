<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isnull`

*Français · [English](isnull.en.md)*

Vrai si la valeur est null ou absente

```
isnull(token)
```

**Exemple**

```jslt
{ "absente": isnull($.z), "vide": isnull($.t) }
```

```json
{ "t": "" }
```

```json
{ "absente": true, "vide": false }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Types, repli sur erreur et validation](../types.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
