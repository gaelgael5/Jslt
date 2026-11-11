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

## Trier et ordonner (`sort`, `reverse`, `first`, `last`)

`limit` tronquait dans l'ordre d'entrée : « les trois plus gros montants » n'était
pas exprimable. `sort(tableau, clef, descendant)` trie, `reverse` inverse (sans
modifier la source), `first` et `last` prennent un bord.

La **clef** est une expression évaluée pour **chaque élément**, l'élément étant la
source courante : `sort($.items, $.prix)` trie sur le prix de chaque élément, et
`sort($.noms, foldtext($))` trie sur une clé calculée. C'est une convention
*différente* de celle de `distinct`, dont le chemin s'applique au tableau entier
(`$.*.prix`) : là, une clé manquante ne pourrait plus être appariée à son élément.
Sans clef, le tri porte sur les éléments eux-mêmes ; pour préciser le sens, la
clef est `$`.

**Ordre total, qui ne lève jamais.** Un tableau de données réelles mélange les
types ; un tri qui refuserait de comparer `null` à une chaîne serait inutilisable
là où on en a le plus besoin. L'ordre est donc : `null` < booléens < nombres <
chaînes < tableaux < objets. Dans un même rang, les nombres se comparent
numériquement, les chaînes par **points de code** (donc « Zoé » avant « école »),
tableaux et objets par leur JSON compact — arbitraire mais stable. Pour un ordre
humain, trier sur une clé pliée (`foldtext`). Le tri est **stable** dans les deux
sens : à clefs égales, l'ordre d'origine survit.

```jslt
{ "top": limit(sort($.ventes, $.montant, true), 2) }
```

```json
{ "ventes": [
  { "ville": "Lyon", "montant": 50 },
  { "ville": "Nice", "montant": 150 },
  { "ville": "Brest", "montant": 90 }
] }
```

```json
{ "top": [ { "ville": "Nice", "montant": 150 }, { "ville": "Brest", "montant": 90 } ] }
```

Un élément dont la clef est absente vaut `null`, donc passe **devant** : les
trous se regroupent là où on les voit, au lieu de faire lever le tri.

## Agréger (`count`, `avg`, `median`, `product`, `min`, `max`)

`sum` était seul, et `min`/`max` étaient **binaires** (deux nombres) : « le plus
petit de la liste » n'existait pas. `min` et `max` acceptent désormais **un
tableau** en plus de leur forme .NET à deux arguments — c'est la même question,
et `sum($.n)` agrège déjà. Avec un tableau, ils conservent le type (un entier
reste entier) ; avec deux nombres, ils gardent le quirk .NET du résultat décimal.
Passer un tableau **et** un second argument lève, plutôt que d'ignorer le second
en silence.

| Fonction | Sur un tableau vide |
|---|---|
| `count(v)` | `0` — et compte aussi les clés d'un objet, les caractères d'un texte |
| `sum(v)` | `0` |
| `product(v)` | `1` (élément neutre) |
| `avg(v)`, `median(v)`, `min(v)`, `max(v)` | `null` — la moyenne de rien n'est pas 0 |

Comme `sum`, tous **lèvent** sur un élément non numérique : un agrégat qui saute
les intrus en silence rend un résultat plausible et faux.

```jslt
{
  "n": count($.v), "total": sum($.v), "moyenne": avg($.v),
  "mediane": median($.v), "mini": min($.v), "maxi": max($.v),
  "clefs": count($.o)
}
```

```json
{ "v": [10, 20, 30, 40], "o": { "a": 1, "b": 2 } }
```

```json
{ "n": 4, "total": 100, "moyenne": 25.0, "mediane": 25.0, "mini": 10, "maxi": 40, "clefs": 2 }
```

---

**Voir aussi** : [Conditions et boucles](conditions-et-boucles.md) pour parcourir
une collection, [Chemins JSONPath](chemins.md) pour la filtrer.

---

[← Guide jslt](guide.md)
