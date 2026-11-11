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
les tableaux **élément par élément** (un préfixe passe devant la séquence qu'il
préfixe : `[1]` avant `[1, 1]`) et les objets par leurs clés triées puis leurs
valeurs. Pour un ordre humain, trier sur une clé pliée (`foldtext`). Le tri est
**stable** dans les deux sens : à clefs égales, l'ordre d'origine survit.

Comme la clef est une expression, elle peut rendre un **tableau** : c'est ainsi
qu'on trie sur plusieurs critères, du plus fort au plus faible.

```jslt
{ "r": selectmany(sort($.l, [$.ville, $.montant]), $.*.id) }
```

```json
{ "l": [
  { "id": 1, "ville": "Lyon", "montant": 20 },
  { "id": 2, "ville": "Brest", "montant": 9 },
  { "id": 3, "ville": "Lyon", "montant": 10 }
] }
```

```json
{ "r": [2, 3, 1] }
```

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

Chaque clef peut avoir **son** sens : le 3ᵉ argument accepte un tableau de
booléens, aligné sur les clefs. Un seul `descendant` ne pouvait pas l'exprimer —
il inverse l'ordre complet, donc toutes les clefs à la fois. Ville croissante,
montant décroissant :

```jslt
{ "r": selectmany(sort($.l, [$.ville, $.montant], [false, true]), $.*.id) }
```

```json
{ "l": [
  { "id": 1, "ville": "Lyon", "montant": 20 },
  { "id": 2, "ville": "Brest", "montant": 9 },
  { "id": 3, "ville": "Lyon", "montant": 50 }
] }
```

```json
{ "r": [2, 3, 1] }
```

Un sens **manquant** vaut croissant, comme l'argument omis ; un sens **en trop**
lève, parce que c'est la faute d'écriture la plus probable et qu'elle laisserait
un tri d'apparence juste. Avec un tableau de sens, la clef doit être un tableau :
sans position, il n'y aurait rien à ordonner par position.

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

## Parcourir et découper (`skip`, `flatten`, `zip`, `unzip`, `chunk`, `window`)

| Fonction | Rôle |
|---|---|
| `skip(l, n)` | ignore les n premiers — le complément de `limit`, sans lequel il n'y a pas de pagination |
| `flatten(l, profondeur)` | aplatit **récursivement** ; `union` ne descend que d'un niveau |
| `zip(a, b)` | apparie, en s'arrêtant au plus court |
| `unzip(l)` | défait l'appariement : une colonne par position |
| `chunk(l, taille)` | tranches consécutives (la dernière peut être plus courte) |
| `window(l, taille)` | fenêtres **glissantes** de taille éléments |
| `indexof(l, v)` / `lastindexof(l, v)` | position d'une valeur, `-1` si absente |

`indexof` et `lastindexof` acceptent désormais un **tableau** en plus d'un texte.
Sur un tableau, l'égalité est **structurelle** : chercher `2` ne trouve pas
`"2"`. `contains`, lui, garde l'égalité `==` du langage pour rester fidèle au
.NET — l'écart est volontaire, et c'est pourquoi les deux cohabitent.

`zip` tronque au plus court plutôt que de compléter par `null` : un appariement
inventé serait indiscernable d'une vraie valeur nulle. `unzip` est sa réciproque
et s'arrête pour la même raison à la rangée la plus courte ; une rangée qui n'est
pas un tableau **lève**, parce que le chemin, lui, était bon. Une taille de
tranche nulle ou négative **lève** aussi (`chunk`, `window`) : c'est une faute
d'écriture.

```jslt
{ "colonnes": unzip($.lignes) }
```

```json
{ "lignes": [[1, "a"], [2, "b"], [3, "c"]] }
```

```json
{ "colonnes": [[1, 2, 3], ["a", "b", "c"]] }
```

```jslt
{
  "page": limit(skip($.l, 2), 2),
  "paires": window($.l, 2) -> limit(2),
  "a_plat": flatten($.imbrique)
}
```

```json
{ "l": [1, 2, 3, 4, 5], "imbrique": [1, [2, [3, [4]]]] }
```

```json
{ "page": [3, 4], "paires": [[1, 2], [2, 3]], "a_plat": [1, 2, 3, 4] }
```

## Séparer et dédupliquer (`partition`, `distinctby`, `intersect`, `difference`)

`partition(l, prédicat)` rend `{ "true": …, "false": … }` : les deux côtés d'un
filtre en une passe, et le lecteur voit qu'ils sont complémentaires.
`distinctby(l, clef)` déduplique sur une clef calculée par élément et garde le
**premier** — ce que `distinct` ne sait pas faire, puisqu'il ignore les objets.

`intersect` et `difference` conservent l'ordre de **gauche** et retirent les
doublons. Comme `indexof` sur tableau, elles comparent la **structure** : sur un
ensemble, confondre `2` et `"2"` rendrait le résultat dépendant de l'ordre des
éléments.

```jslt
{
  "tri": partition($.l, $.actif),
  "clients": distinctby($.l, $.client) -> count(),
  "communs": intersect($.a, $.b)
}
```

```json
{
  "l": [
    { "client": 1, "actif": true },
    { "client": 2, "actif": false },
    { "client": 1, "actif": true }
  ],
  "a": [3, 1, 3],
  "b": [1, 3]
}
```

```json
{
  "tri": {
    "true": [{ "client": 1, "actif": true }, { "client": 1, "actif": true }],
    "false": [{ "client": 2, "actif": false }]
  },
  "clients": 2,
  "communs": [3, 1]
}
```

## Dispersion, quantiles et mode

| Fonction | Rôle |
|---|---|
| `variance(v, échantillon)` | variance de **population** par défaut ; `true` pour la correction de Bessel (n-1) |
| `stddev(v, échantillon)` | écart-type, même convention |
| `percentile(v, p)` | centile de 0 à 100, par **interpolation linéaire** |
| `mode(v)` | valeur la plus fréquente |

La population est le défaut parce qu'un template transforme **les données qu'on
lui donne** : elles sont l'ensemble, pas un tirage. La variance d'échantillon
d'une valeur unique vaut `null` (n-1 = 0) — la question n'a pas de réponse, et 0
affirmerait une dispersion nulle.

`percentile` interpole linéairement, méthode explicite parce qu'il en existe
neuf : `percentile(v, 50)` coïncide donc avec `median`. `mode` accepte
**n'importe quelles** valeurs, pas seulement des nombres — la valeur modale d'un
libellé a un sens, et c'est son usage principal ; à égalité, le premier apparu
gagne.

```jslt
{
  "ecart": stddev($.v),
  "p90": percentile($.v, 90),
  "frequent": mode($.t)
}
```

```json
{ "v": [2, 4, 4, 4, 5, 5, 7, 9], "t": ["a", "b", "b"] }
```

```json
{ "ecart": 2.0, "p90": 7.6, "frequent": "b" }
```

## Agréger par groupe (`groupby`, `countby`, `sumby`, `avgby`)

`group` rend la forme .NET (`Label` / `Items`). `groupby(l, clef)` rend un
**objet** `{ clef: éléments }`, qui se parcourt avec `entries` : l'agrégation par
groupe tient alors dans une expression. `countby` fait directement le cas le plus
fréquent. La clef est convertie en texte, puisqu'une clé d'objet JSON est une
chaîne.

```jslt
{
  "par_ville": countby($.l, $.ville),
  "totaux": fromentries([
    { "$source": entries(groupby($.l, $.ville)),
      "key": $.key,
      "value": sum(selectmany($.value, $.*.m)) }
  ])
}
```

```json
{ "l": [
  { "ville": "Lyon", "m": 10 },
  { "ville": "Nice", "m": 20 },
  { "ville": "Lyon", "m": 5 }
] }
```

```json
{ "par_ville": { "Lyon": 2, "Nice": 1 }, "totaux": { "Lyon": 15, "Nice": 20 } }
```

`sumby` et `avgby` font ce total directement : c'est l'usage le plus fréquent du
regroupement, et il demandait quatre fonctions imbriquées. La clef se calcule par
élément comme pour `sort` ; le 3ᵉ argument est la **valeur** à agréger, et s'il
est omis c'est l'élément lui-même — un tableau de nombres s'agrège donc sans lui.
Une valeur non numérique **lève**, comme pour `sum` : un total qui saute les
intrus est plausible et faux.

Une clef composite rend une clef **textuelle** (`["FR","Lyon"]`, en JSON
compact). Pour la relire par chemin, `groupby` **imbrique** un niveau par clef
quand son 3ᵉ argument vaut `true` :

```jslt
{
  "totaux": sumby($.l, $.pays, $.m),
  "par_pays": groupby($.l, [$.pays, $.ville], true)
}
```

```json
{ "l": [
  { "pays": "FR", "ville": "Lyon", "m": 10 },
  { "pays": "FR", "ville": "Nice", "m": 20 },
  { "pays": "BE", "ville": "Gand", "m": 7 }
] }
```

```json
{
  "totaux": { "FR": 30, "BE": 7 },
  "par_pays": {
    "FR": { "Lyon": [{ "pays": "FR", "ville": "Lyon", "m": 10 }],
            "Nice": [{ "pays": "FR", "ville": "Nice", "m": 20 }] },
    "BE": { "Gand": [{ "pays": "BE", "ville": "Gand", "m": 7 }] }
  }
}
```

Imbriquer exige un tableau de clefs, et le **même nombre** de clefs pour tous les
éléments : sinon une même clef porterait à la fois des éléments et un sous-groupe,
et l'un des deux disparaîtrait.

---

**Voir aussi** : [Conditions et boucles](conditions-et-boucles.md) pour parcourir
une collection, [Chemins JSONPath](chemins.md) pour la filtrer.

---

[← Guide jslt](guide.md)
