# Données et collections — guide jslt

*Français · [English](collections.en.md)*

[← Guide jslt](guide.md) · les exemples de cette page sont **exécutés par la
suite de tests** (`tests/test_guide_examples.py`), sous la forme de triplets
*template → entrée → sortie*.

---

## Cœur : `sum`, `concat`, `distinct`

`sum` additionne les éléments d'un tableau (reste entier si tout est entier) :

```jslt
{ "total": sum($.n) }
```
```json
{ "n": [1, 2, 3] }
```
```json
{ "total": 6 }
```

`concat(tableau)` joint les éléments en chaîne ; un second argument sert de
séparateur :

```jslt
{ "colle": concat($.parts), "joint": concat($.parts, "-") }
```
```json
{ "parts": ["a", "b", "c"] }
```
```json
{ "colle": "abc", "joint": "a-b-c" }
```

`distinct(source, chemin)` déduplique les valeurs sélectionnées par le chemin
(le second argument est un **chemin compilé**, appliqué à `source`) :

```jslt
{ "uniques": distinct($.vals, $.*) }
```
```json
{ "vals": [1, 2, 2, 3, 3, 3] }
```
```json
{ "uniques": [1, 2, 3] }
```

---

## Tests sur les collections : `any`, `contains`, `selectany`

`any(tableau)` est vrai pour un tableau non vide ; `contains(tableau, valeur)`
compare avec l'égalité de l'opérateur `==` ; `selectany(source, "chemin")` est
vrai si le chemin JSONPath (écrit en chaîne, comme en .NET, ou directement)
sélectionne au moins une valeur.

```jslt
{ "plein": any($.a), "a_b": contains($.a, "b"), "grand": selectany($.n, "$[?(@ > 2)]") }
```
```json
{ "a": ["a", "b"], "n": [1, 3] }
```
```json
{ "plein": true, "a_b": true, "grand": true }
```

---

## Collections : `limit`, `union`, `select`, `selectmany`

```jslt
{ "deux": limit($.a, 2), "aplati": union($.groups) }
```
```json
{ "a": [1, 2, 3, 4], "groups": [[1, 2], [3, 4], [5]] }
```
```json
{ "deux": [1, 2], "aplati": [1, 2, 3, 4, 5] }
```

`select(source, chemin)` renvoie la **première** valeur sélectionnée ;
`selectmany(source, chemin)` les renvoie **toutes** (chemin compilé) :

```jslt
{ "premier": select($.items, $.*.n), "tous": selectmany($.items, $.*.n) }
```
```json
{ "items": [ { "n": 1 }, { "n": 2 } ] }
```
```json
{ "premier": 1, "tous": [1, 2] }
```

`selectmany` est aussi la façon de construire un **tableau de valeurs simples**
à partir d'une collection filtrée, là où une boucle `$source` ne produirait que
des objets — voir [Conditions et boucles](conditions-et-boucles.md).

---

## Regroupement et jointure : `group`, `join`, `createindex`, `index`

`group(tableau, ["$.chemin", …])` rend des groupes `{ "Label", "Items" }`,
imbriqués quand plusieurs chemins sont donnés. `join(gauche, $.clé, false,
[{ "Name", "Key", "Source" }])` rattache à chaque objet de gauche, sous `Name`,
les éléments de `Source` dont la clé `Key` est égale (comparée en texte) ; la
source n'est pas modifiée. `createindex(source, découpe, "$.clé")` construit un
index que `index(i, clé)` interroge.

```jslt
{ "parVille": group($.p, ["$.city"]), "i:": createindex($.p, "", "$.name"), "bob": index(i:, "Bob") }
```
```json
{ "p": [{ "name": "Ana", "city": "Lyon" }, { "name": "Bob", "city": "Paris" }] }
```
```json
{ "parVille": [{ "Label": "Lyon", "Items": [{ "name": "Ana", "city": "Lyon" }] }, { "Label": "Paris", "Items": [{ "name": "Bob", "city": "Paris" }] }], "bob": { "name": "Bob", "city": "Paris" } }
```

```jslt
{ "clients": join($.c, $.id, false, [{ "Name": "commandes", "Key": "$.client", "Source": $.o }]) }
```
```json
{ "c": [{ "id": 1, "nom": "Ana" }], "o": [{ "client": 1, "total": 12 }, { "client": 2, "total": 5 }] }
```
```json
{ "clients": [{ "id": 1, "nom": "Ana", "commandes": [{ "total": 12 }] }] }
```

---

## Schéma : `schema`

`schema(exemple)` déduit un JSON Schema (draft-04) d'un fragment JSON, comme
NJsonSchema côté .NET : objets imbriqués en `definitions` référencées.

```jslt
{ "s": schema($.exemple) }
```
```json
{ "exemple": { "nom": "Ana", "age": 30 } }
```
```json
{ "s": { "$schema": "http://json-schema.org/draft-04/schema#", "type": "object", "properties": { "nom": { "type": "string" }, "age": { "type": "integer" } } } }
```


---

**Voir aussi** : [Conditions et boucles](conditions-et-boucles.md) pour parcourir
une collection, [Chemins JSONPath](chemins.md) pour la filtrer.

---

[← Guide jslt](guide.md)
