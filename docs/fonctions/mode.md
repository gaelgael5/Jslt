<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `mode`

*Français · [English](mode.en.md)*

Valeur la plus fréquente d'un tableau (la première apparue en cas d'égalité)

```
mode(token)
```

**Exemple**

```jslt
{ "r": mode($.l) }
```

```json
{ "l": ["a", "b", "a"] }
```

```json
{ "r": "a" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**À savoir**

- Accepte **toutes** les valeurs, pas seulement des nombres : la plus fréquente d'un libellé a un sens. À égalité, la **première apparue** gagne.

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
