# Chemins JSONPath — guide jslt

*Français · [English](chemins.en.md)*

[← Guide jslt](guide.md) · les exemples de cette page sont **exécutés par la
suite de tests** (`tests/test_guide_examples.py`), sous la forme de triplets
*template → entrée → sortie*.

---

## Lire la source

`$` est la racine du document source. On navigue avec `.clé`, `[indice]`,
`[début:fin]` (slice), `*` (wildcard) et `..` (descente récursive).

### Accès par clé

```jslt
{ "nom": $.user.name, "age": $.user.age }
```
```json
{ "user": { "name": "Alice", "age": 30 } }
```
```json
{ "nom": "Alice", "age": 30 }
```

### Indice, slice, wildcard

```jslt
{ "premier": $.items[0], "slice": $.items[1:3], "wild": $.obj.* }
```
```json
{ "items": [10, 20, 30, 40], "obj": { "x": 1, "y": 2 } }
```
```json
{ "premier": 10, "slice": [20, 30], "wild": [1, 2] }
```

### Descente récursive `..`

`$..id` collecte **tous** les `id`, à n'importe quelle profondeur, dans l'ordre
de parcours du document (un nœud est inspecté avant ses enfants) :

```jslt
{ "ids": $..id }
```
```json
{ "a": { "id": 1 }, "b": { "nested": { "id": 2 } }, "c": { "id": 3 } }
```
```json
{ "ids": [1, 2, 3] }
```

---

## Sémantique 0 / 1 / N

Un chemin (ou un filtre) peut sélectionner **0, 1 ou N** valeurs. Le résultat
suit la règle du moteur .NET (`GetContentByJPath`) :

| Correspondances | Résultat |
|---|---|
| 0 | `null` |
| 1 | la valeur (pas une liste d'un élément) |
| N | la liste des valeurs |

Zéro correspondance → `null` :

```jslt
{ "r": $.inconnu }
```
```json
{ "a": 1 }
```
```json
{ "r": null }
```

Une seule correspondance → la valeur directement :

```jslt
{ "r": $.items[?(@.n == 2)] }
```
```json
{ "items": [ { "n": 1 }, { "n": 2 }, { "n": 3 } ] }
```
```json
{ "r": { "n": 2 } }
```

Plusieurs correspondances → une liste :

```jslt
{ "r": $.items[?(@.n >= 2)] }
```
```json
{ "items": [ { "n": 1 }, { "n": 2 }, { "n": 3 } ] }
```
```json
{ "r": [ { "n": 2 }, { "n": 3 } ] }
```

---

## Filtres JSONPath `?(...)`

`$.items[?(cond)]` ne garde que les éléments vérifiant `cond`. Dans la condition,
`@` désigne l'élément courant et `$` la racine du document. Opérateurs :
comparaisons `== != < <= > >=`, logiques `&` (et) / `|` (ou), appartenance `in`.

```jslt
{ "grands": $.items[?(@.n > 1)] }
```
```json
{ "items": [ { "n": 1 }, { "n": 2 }, { "n": 3 } ] }
```
```json
{ "grands": [ { "n": 2 }, { "n": 3 } ] }
```

Et logique `&` (ici une seule correspondance → la valeur, cf.
[Sémantique 0 / 1 / N](#sémantique-0--1--n)) :

```jslt
{ "r": $.items[?(@.ok == true & @.n > 1)] }
```
```json
{ "items": [ { "n": 1, "ok": true }, { "n": 3, "ok": true } ] }
```
```json
{ "r": { "n": 3, "ok": true } }
```

Appartenance `in` à un littéral ou à un chemin :

```jslt
{ "autorises": $.items[?(@.id in [2, 3])] }
```
```json
{ "items": [ { "id": 1 }, { "id": 2 }, { "id": 3 } ] }
```
```json
{ "autorises": [ { "id": 2 }, { "id": 3 } ] }
```

Comparaison à une valeur de la racine :

```jslt
{ "r": $.items[?(@.n >= $.seuil)] }
```
```json
{ "items": [ { "n": 1 }, { "n": 2 }, { "n": 3 } ], "seuil": 2 }
```
```json
{ "r": [ { "n": 2 }, { "n": 3 } ] }
```

Un filtre alimente couramment une boucle :

```jslt
[ { "$source": $.items[?(@.ok == true)], "v": $.n } ]
```
```json
{ "items": [ { "n": 1, "ok": true }, { "n": 2, "ok": false }, { "n": 3, "ok": true } ] }
```
```json
[ { "v": 1 }, { "v": 3 } ]
```

---

## Fonctions de chemin `length()` / `value()`

À la fin d'un chemin, `length()` donne la taille (tableau, objet ou chaîne ;
`null` pour un scalaire non mesurable) et `value()` renvoie la valeur telle
quelle. Utilisables aussi dans les filtres.

```jslt
{ "taille": $.tags.length(), "valeur": $.v.value() }
```
```json
{ "tags": ["a", "b", "c"], "v": 42 }
```
```json
{ "taille": 3, "valeur": 42 }
```

Dans un filtre :

```jslt
{ "r": $.items[?(@.tags.length() > 1)] }
```
```json
{ "items": [ { "tags": ["x"] }, { "tags": ["y", "z"] } ] }
```
```json
{ "r": { "tags": ["y", "z"] } }
```


---

[← Guide jslt](guide.md)
