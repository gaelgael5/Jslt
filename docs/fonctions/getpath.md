<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `getpath`

*Français · [English](getpath.en.md)*

Valeur au bout d'un chemin pointé calculé (null si une étape manque)

```
getpath(token, path, separator)
```

**Exemple**

```jslt
{ "r": getpath($.o, $.champ) }
```

```json
{ "o": { "client": { "ville": "Lyon" } }, "champ": "client.ville" }
```

```json
{ "r": "Lyon" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel | l'objet ou le tableau de départ ; autre chose rend `null` |
| `path` | optionnel | le chemin pointé, **calculable** (`"client.ville"`, `"lignes.0.ref"`) ; mêmes étapes que `setpath` |
| `separator` | optionnel | séparateur des étapes, `.` par défaut ; vide, il lève |

**À savoir**

- Réciproque de `setpath`, qui n'en avait pas : les étapes se lisent de la même façon, indices de tableau compris (`"lignes.0.ref"`).
- Une étape manquante — ou un scalaire rencontré en cours de route — rend `null` sans lever : c'est la sémantique d'un chemin, et `??` fournit le repli.

**Chapitre** : [Objets et structures profondes](../objets.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
