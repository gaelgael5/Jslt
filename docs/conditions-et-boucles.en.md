# Conditionals and loops — jslt guide

*[Français](conditions-et-boucles.md) · English*

[← jslt guide](guide.en.md) · the examples on this page are **run by the test
suite** (`tests/test_guide_examples.py`) as *template → input → output* triples.

---

## `when` / `switch`

`when(expr) { "case": block, ..., "default": block }` compares `expr` (`==`) to
each case name and returns the block of the first matching case; otherwise
`default`; otherwise `null`. `switch` is an **alias** of `when`. The comparison
coerces types, so a numeric code matches a textual case name.

```jslt
{ "statut": when($.code) { "200": "ok", "404": "introuvable", "default": "autre" } }
```
```json
{ "code": 404 }
```
```json
{ "statut": "introuvable" }
```

With no matching case and no `default`, the result is `null`:

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

## Loops `$source` / `$where`

An array containing **one object** with a `"$source"` is a **loop**: the object is
produced for each element of `$source`, and `$` there denotes the **current
element**. `"$where"` filters the elements (keeps only those whose expression is
true).

```jslt
[ { "$source": $.users, "nom": $.name, "majeur": $.age >= 18 } ]
```
```json
{ "users": [ { "name": "A", "age": 30 }, { "name": "B", "age": 15 } ] }
```
```json
[ { "nom": "A", "majeur": true }, { "nom": "B", "majeur": false } ]
```

With `$where` to keep only the active ones:

```jslt
[ { "$source": $.users, "$where": $.actif, "nom": $.name } ]
```
```json
{ "users": [ { "name": "A", "actif": true }, { "name": "B", "actif": false } ] }
```
```json
[ { "nom": "A" } ]
```


### Array of plain values (no wrapper object)

A loop always produces **objects**: the loop body *is* the object carrying the
`$source`, and there is no scalar-body form (a `"$value"` key would be ignored,
like any unknown `$xxx` key). To get an array of strings or numbers, do not
loop: project a path with
[`selectmany`](collections.en.md#collections-limit-union-select-selectmany).

```jslt
{ "references": selectmany($, $.produits[?(@.disponible in [true, "true"])].reference) }
```
```json
{ "produits": [ { "reference": "A-100", "disponible": true }, { "reference": "B-200", "disponible": "true" }, { "reference": "C-300", "disponible": false } ] }
```
```json
{ "references": ["A-100", "B-200"] }
```

The bare path (`$.produits[?(…)].reference`) gives the same result **from two
matches on**, but it follows the 0 / 1 / N semantics
([Paths](chemins.en.md#0--1--n-semantics)): a single match yields
the value alone, no match yields `null`.

```jslt
{ "references": $.produits[?(@.disponible == true)].reference }
```
```json
{ "produits": [ { "reference": "A-100", "disponible": true } ] }
```
```json
{ "references": "A-100" }
```

That is the trap when the output field is expected to be a list: `selectmany`
always returns an array, `[]` included.

```jslt
{ "references": selectmany($, $.produits[?(@.disponible == true)].reference) }
```
```json
{ "produits": [ { "reference": "A-100", "disponible": true } ] }
```
```json
{ "references": ["A-100"] }
```

To deduplicate the projection, `distinct` applies its path **to the array it
receives** (not to the document): the path is therefore relative to that array.

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

[← jslt guide](guide.en.md)
