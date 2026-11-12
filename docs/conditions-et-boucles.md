# Conditions et boucles — guide jslt

*Français · [English](conditions-et-boucles.en.md)*

[← Guide jslt](guide.md) · les exemples de cette page sont **exécutés par la
suite de tests** (`tests/test_guide_examples.py`), sous la forme de triplets
*template → entrée → sortie*.

---

## Choisir une valeur : `ifelse`

`ifelse(condition, si_vrai, si_faux)` est la conditionnelle en position
d'**expression**. C'est ce que `when` ne fait pas : `when` aiguille sur une
**valeur** (il compare `==` au nom de chaque cas), donc une condition composée
devait d'abord être calculée, puis aiguillée sur son texte `"true"` / `"false"`.

```jslt
{ "mention": ifelse($.note >= 10 && $.present, "admis", "ajourné") }
```
```json
{ "note": 12, "present": true }
```
```json
{ "mention": "admis" }
```

Seule la branche **retenue** est évaluée, et c'est tout l'intérêt : la branche
écartée peut lever sans conséquence, donc `ifelse($.d == 0, 0, 100 / $.d)` est
sûr même quand le diviseur est nul. Pour plus de deux cas, `ifelse` s'imbrique ;
dès que les cas sont des **valeurs** d'un même champ, `when` reprend la main et
se lit mieux.

```jslt
{ "palier": ifelse($.n < 0, "négatif", ifelse($.n == 0, "nul", "positif")), "ratio": ifelse($.d == 0, 0, 100 / $.d) }
```
```json
{ "n": 0, "d": 0 }
```
```json
{ "palier": "nul", "ratio": 0 }
```

La condition se lit comme celle de [`filter`](collections.md#parcourir-par-expression-map-filter-find-every-some-reduce)
et non comme une assertion : `null`, `0`, `""`, un tableau ou un objet vide sont
**faux**, et le texte `"false"` aussi. Une troisième branche absente rend `null`,
comme un `when` sans `default`.

---

## `when` / `switch`

`when(expr) { "cas": bloc, ..., "default": bloc }` compare `expr` (`==`) au nom de
chaque cas et renvoie le bloc du premier cas correspondant ; sinon `default` ;
sinon `null`. `switch` est un **alias** de `when`. La comparaison coerce les
types, donc un code numérique matche un nom de cas textuel.

```jslt
{ "statut": when($.code) { "200": "ok", "404": "introuvable", "default": "autre" } }
```
```json
{ "code": 404 }
```
```json
{ "statut": "introuvable" }
```

Sans cas correspondant ni `default`, le résultat est `null` :

```jslt
{ "statut": when($.code) { "200": "ok" } }
```
```json
{ "code": 500 }
```
```json
{ "statut": null }
```

---

## Boucles `$source` / `$where`

Un tableau contenant **un objet** doté de `"$source"` est une **boucle** : l'objet
est produit pour chaque élément de `$source`, et `$` y désigne l'**élément
courant**. `"$where"` filtre les éléments (ne garde que ceux dont l'expression est
vraie).

```jslt
[ { "$source": $.users, "nom": $.name, "majeur": $.age >= 18 } ]
```
```json
{ "users": [ { "name": "A", "age": 30 }, { "name": "B", "age": 15 } ] }
```
```json
[ { "nom": "A", "majeur": true }, { "nom": "B", "majeur": false } ]
```

Avec `$where` pour ne garder que les actifs :

```jslt
[ { "$source": $.users, "$where": $.actif, "nom": $.name } ]
```
```json
{ "users": [ { "name": "A", "actif": true }, { "name": "B", "actif": false } ] }
```
```json
[ { "nom": "A" } ]
```


### Tableau de valeurs simples (sans objet enveloppe)

Une boucle produit toujours des **objets** : le corps de la boucle *est* l'objet
qui porte le `$source`, il n'existe pas de forme à corps scalaire (une clé
`"$valeur"` serait d'ailleurs ignorée, comme toute clé `$xxx` inconnue). Pour
obtenir un tableau de chaînes ou de nombres, on ne boucle pas : on projette un
chemin avec [`selectmany`](collections.md#collections--limit-union-select-selectmany).

```jslt
{ "references": selectmany($, $.produits[?(@.disponible in [true, "true"])].reference) }
```
```json
{ "produits": [ { "reference": "A-100", "disponible": true }, { "reference": "B-200", "disponible": "true" }, { "reference": "C-300", "disponible": false } ] }
```
```json
{ "references": ["A-100", "B-200"] }
```

Le chemin nu (`$.produits[?(…)].reference`) donne le même résultat **à partir de
deux correspondances**, mais il suit la sémantique 0 / 1 / N
([Chemins](chemins.md#sémantique-0--1--n)) : une seule
correspondance rend la valeur seule, aucune rend `null`.

```jslt
{ "references": $.produits[?(@.disponible == true)].reference }
```
```json
{ "produits": [ { "reference": "A-100", "disponible": true } ] }
```
```json
{ "references": "A-100" }
```

C'est le piège quand le champ de sortie est attendu comme une liste :
`selectmany` rend toujours un tableau, `[]` compris.

```jslt
{ "references": selectmany($, $.produits[?(@.disponible == true)].reference) }
```
```json
{ "produits": [ { "reference": "A-100", "disponible": true } ] }
```
```json
{ "references": ["A-100"] }
```

Pour dédoublonner la projection, `distinct` applique son chemin **au tableau
reçu** (pas au document) : le chemin est donc relatif à ce tableau.

```jslt
{ "references": distinct($.produits[?(@.disponible == true)], $[*].reference) }
```
```json
{ "produits": [ { "reference": "A-100", "disponible": true }, { "reference": "B-200", "disponible": true }, { "reference": "A-100", "disponible": true }, { "reference": "C-300", "disponible": false } ] }
```
```json
{ "references": ["A-100", "B-200"] }
```


---

[← Guide jslt](guide.md)
