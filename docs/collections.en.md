# Data and collections — jslt guide

*[Français](collections.md) · English*

[← jslt guide](guide.en.md) · the examples on this page are **run by the test
suite** (`tests/test_guide_examples.py`) as *template → input → output* triples.

---

## Core: `sum`, `concat`, `distinct`

`sum` adds up the elements of an array (stays an integer if everything is integer):

```jslt
{ "total": sum($.n) }
```
```json
{ "n": [1, 2, 3] }
```
```json
{ "total": 6 }
```

`concat(array)` joins the elements into a string; a second argument is used as a
separator:

```jslt
{ "colle": concat($.parts), "joint": concat($.parts, "-") }
```
```json
{ "parts": ["a", "b", "c"] }
```
```json
{ "colle": "abc", "joint": "a-b-c" }
```

`distinct(source, path)` deduplicates the values selected by the path (the second
argument is a **compiled path**, applied to `source`):

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

## Collection tests: `any`, `contains`, `selectany`

`any(array)` is true for a non-empty array; `contains(array, value)` compares
with the `==` operator's equality; `selectany(source, "path")` is true when the
JSONPath (written as a string or directly) selects at least one
value.

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

## Collections: `limit`, `union`, `select`, `selectmany`

```jslt
{ "deux": limit($.a, 2), "aplati": union($.groups) }
```
```json
{ "a": [1, 2, 3, 4], "groups": [[1, 2], [3, 4], [5]] }
```
```json
{ "deux": [1, 2], "aplati": [1, 2, 3, 4, 5] }
```

`select(source, path)` returns the **first** selected value; `selectmany(source,
path)` returns **all** of them (compiled path):

```jslt
{ "premier": select($.items, $.*.n), "tous": selectmany($.items, $.*.n) }
```
```json
{ "items": [ { "n": 1 }, { "n": 2 } ] }
```
```json
{ "premier": 1, "tous": [1, 2] }
```

`selectmany` is also the way to build an **array of plain values** out of a
filtered collection, where a `$source` loop would only produce objects — see
[Conditionals and loops](conditions-et-boucles.en.md).

---

## Grouping and joins: `group`, `join`, `createindex`, `index`

`group(array, ["$.path", …])` returns `{ "Label", "Items" }` groups, nested
when several paths are given. `join(left, $.key, false, [{ "Name", "Key",
"Source" }])` attaches to each left object, under `Name`, the `Source` items
whose `Key` is equal (compared as text); the source is not modified.
`createindex(source, split, "$.key")` builds an index queried by
`index(i, key)`.

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

## Sorting and ordering (`sort`, `reverse`, `first`, `last`)

`limit` truncated in input order: "the three largest amounts" was not
expressible. `sort(array, key, descending)` sorts, `reverse` reverses (without
modifying the source), `first` and `last` take an edge.

The **key** is an expression evaluated for **each element**, with the element as
the current source: `sort($.items, $.price)` sorts on each element's price, and
`sort($.names, foldtext($))` sorts on a computed key. This is a convention
*different* from `distinct`, whose path applies to the whole array (`$.*.price`):
there, a missing key could no longer be paired with its element. With no key the
sort is on the elements themselves; to state the direction, the key is `$`.

**A total order that never raises.** An array of real data mixes types; a sort
refusing to compare `null` with a string would be useless exactly where it is
needed. The order is therefore: `null` < booleans < numbers < strings < arrays <
objects. Within a rank, numbers compare numerically, strings by **code point**
(so "Zoé" before "école"), arrays **element by element** (a prefix comes before
the sequence it prefixes: `[1]` before `[1, 1]`) and objects by their sorted keys
then their values. For a human order, sort on a folded key (`foldtext`). The sort
is **stable** both ways: equal keys keep their original order.

Since the key is an expression, it can return an **array**: that is how you sort
on several criteria, strongest first.

```jslt
{ "r": selectmany(sort($.l, [$.city, $.amount]), $.*.id) }
```

```json
{ "l": [
  { "id": 1, "city": "Lyon", "amount": 20 },
  { "id": 2, "city": "Brest", "amount": 9 },
  { "id": 3, "city": "Lyon", "amount": 10 }
] }
```

```json
{ "r": [2, 3, 1] }
```

```jslt
{ "top": limit(sort($.sales, $.amount, true), 2) }
```

```json
{ "sales": [
  { "city": "Lyon", "amount": 50 },
  { "city": "Nice", "amount": 150 },
  { "city": "Brest", "amount": 90 }
] }
```

```json
{ "top": [ { "city": "Nice", "amount": 150 }, { "city": "Brest", "amount": 90 } ] }
```

Each key can have **its own** direction: the 3rd argument accepts an array of
booleans, aligned with the keys. A single `descending` could not express that —
it reverses the whole order, hence every key at once. City ascending, amount
descending:

```jslt
{ "r": selectmany(sort($.l, [$.city, $.amount], [false, true]), $.*.id) }
```

```json
{ "l": [
  { "id": 1, "city": "Lyon", "amount": 20 },
  { "id": 2, "city": "Brest", "amount": 9 },
  { "id": 3, "city": "Lyon", "amount": 50 }
] }
```

```json
{ "r": [2, 3, 1] }
```

A **missing** direction means ascending, like the omitted argument; a direction
**too many** raises, because that is the likeliest authoring mistake and it would
leave a sort that looks right. With an array of directions the key must be an
array: with no positions there would be nothing to order per position.

An element whose key is missing counts as `null`, so it comes **first**: gaps
gather where you can see them, instead of making the sort raise.

## Aggregating (`count`, `avg`, `median`, `product`, `min`, `max`)

`sum` was alone, and `min`/`max` were **binary** (two numbers): "the smallest in
the list" did not exist. `min` and `max` now accept **an array** in addition to
their two-argument form — it is the same question, and `sum($.n)` already
aggregates. Given an array they preserve the type (an integer stays an integer);
given two numbers they return a **decimal**, a convention kept from their
original form. Passing an array
**and** a second argument raises, rather than silently ignoring the second.

| Function | On an empty array |
|---|---|
| `count(v)` | `0` — also counts an object's keys, a string's characters |
| `sum(v)` | `0` |
| `product(v)` | `1` (neutral element) |
| `avg(v)`, `median(v)`, `min(v)`, `max(v)` | `null` — the average of nothing is not 0 |

Like `sum`, they all **raise** on a non-numeric element: an aggregate that
silently skips intruders returns a plausible, wrong result.

```jslt
{
  "n": count($.v), "total": sum($.v), "mean": avg($.v),
  "median": median($.v), "min": min($.v), "max": max($.v),
  "keys": count($.o)
}
```

```json
{ "v": [10, 20, 30, 40], "o": { "a": 1, "b": 2 } }
```

```json
{ "n": 4, "total": 100, "mean": 25.0, "median": 25.0, "min": 10, "max": 40, "keys": 2 }
```

---

## Walking and slicing (`skip`, `flatten`, `zip`, `unzip`, `chunk`, `window`)

| Function | Purpose |
|---|---|
| `skip(l, n)` | drops the first n — the complement of `limit`, without which there is no pagination |
| `flatten(l, depth)` | flattens **recursively**; `union` only descends one level |
| `zip(a, b)` | pairs up, stopping at the shorter one |
| `unzip(l)` | undoes the pairing: one column per position |
| `chunk(l, size)` | consecutive slices (the last one may be shorter) |
| `window(l, size)` | **sliding** windows of size elements |
| `indexof(l, v)` / `lastindexof(l, v)` | position of a value, `-1` if absent |

`indexof` and `lastindexof` now accept an **array** as well as text. On an array
the equality is **structural**: searching for `2` does not find `"2"`.
`contains`, by contrast, keeps the language's `==` equality, where `"2" == 2` is
true — the discrepancy is deliberate, and that is why both exist.

`zip` truncates to the shorter rather than padding with `null`: an invented pair
would be indistinguishable from a genuine null value. `unzip` is its converse and
stops at the shortest row for the same reason; a row that is not an array
**raises**, because the path itself was right. A zero or negative slice size
**raises** too (`chunk`, `window`): that is an authoring mistake.

```jslt
{ "columns": unzip($.rows) }
```

```json
{ "rows": [[1, "a"], [2, "b"], [3, "c"]] }
```

```json
{ "columns": [[1, 2, 3], ["a", "b", "c"]] }
```

```jslt
{
  "page": limit(skip($.l, 2), 2),
  "pairs": window($.l, 2) -> limit(2),
  "flat": flatten($.nested)
}
```

```json
{ "l": [1, 2, 3, 4, 5], "nested": [1, [2, [3, [4]]]] }
```

```json
{ "page": [3, 4], "pairs": [[1, 2], [2, 3]], "flat": [1, 2, 3, 4] }
```

## Splitting and deduplicating (`partition`, `distinctby`, `intersect`, `difference`)

`partition(l, predicate)` returns `{ "true": …, "false": … }`: both sides of a
filter in one pass, and the reader sees they are complementary.
`distinctby(l, key)` deduplicates on a key computed per element and keeps the
**first** — which `distinct` cannot do, since it ignores objects.

`intersect` and `difference` keep the **left** order and drop duplicates. Like
`indexof` on an array, they compare the **structure**: in a set, conflating `2`
and `"2"` would make the result depend on element order.

```jslt
{
  "split": partition($.l, $.active),
  "clients": distinctby($.l, $.client) -> count(),
  "common": intersect($.a, $.b)
}
```

```json
{
  "l": [
    { "client": 1, "active": true },
    { "client": 2, "active": false },
    { "client": 1, "active": true }
  ],
  "a": [3, 1, 3],
  "b": [1, 3]
}
```

```json
{
  "split": {
    "true": [{ "client": 1, "active": true }, { "client": 1, "active": true }],
    "false": [{ "client": 2, "active": false }]
  },
  "clients": 2,
  "common": [3, 1]
}
```

## Dispersion, quantiles and mode

| Function | Purpose |
|---|---|
| `variance(v, sample)` | **population** variance by default; `true` for Bessel's correction (n-1) |
| `stddev(v, sample)` | standard deviation, same convention |
| `percentile(v, p)` | percentile from 0 to 100, by **linear interpolation** |
| `mode(v)` | most frequent value |

Population is the default because a template transforms **the data it is
given**: that data is the whole set, not a draw. The sample variance of a single
value is `null` (n-1 = 0) — the question has no answer, and 0 would assert zero
dispersion.

`percentile` interpolates linearly, a method stated explicitly because there are
nine of them: `percentile(v, 50)` therefore agrees with `median`. `mode` accepts
**any** values, not only numbers — the modal value of a label is meaningful, and
that is its main use; on a tie, the first one seen wins.

```jslt
{
  "spread": stddev($.v),
  "p90": percentile($.v, 90),
  "frequent": mode($.t)
}
```

```json
{ "v": [2, 4, 4, 4, 5, 5, 7, 9], "t": ["a", "b", "b"] }
```

```json
{ "spread": 2.0, "p90": 7.6, "frequent": "b" }
```

## Walking with an expression (`map`, `filter`, `find`, `every`, `some`, `reduce`)

The `{"$source": …}` loop does the job of `map`, but only in **value position**:
it cannot be passed as an argument. This family takes an **expression evaluated
per element**, like `sort`'s key, and can therefore be used anywhere.

| Function | Returns |
|---|---|
| `map(l, expr)` | an array of the same length |
| `filter(l, pred)` | the elements whose predicate is true |
| `find(l, pred)` / `findindex(l, pred)` | the first element / its position, `null` / `-1` otherwise |
| `some(l, pred)` / `every(l, pred)` | at least one / all (true on an empty array) |
| `reduce(l, expr, initial)` | **one** value, the expression seeing `{acc, value, index}` |
| `minby(l, key)` / `maxby(l, key)` | the **element** carrying the extremum |
| `cumsum(l)` | the running totals |

`some` does not replace `any`, which says "non-empty array"; and `filter` does
not replace the JSONPath filter `$.l[?(…)]`, which is shorter — but a filter
cannot call a function.

```jslt
{
  "noms": map($.l, $.n),
  "majeurs": map(filter($.l, $.age >= 18), $.n),
  "total": reduce($.l, $.acc + $.value.age, 0),
  "plus_jeune": map([minby($.l, $.age)], $.n)
}
```

```json
{ "l": [{ "n": "Ana", "age": 30 }, { "n": "Bo", "age": 15 }] }
```

```json
{ "noms": ["Ana", "Bo"], "majeurs": ["Ana"], "total": 45, "plus_jeune": ["Bo"] }
```

`reduce` is the engine's only **general fold**: `sum`, `product` and `sumby` are
special cases of it. The accumulator and the element are presented together as
the current source (`$.acc`, `$.value`, `$.index`), because an expression has
only one source and the language has no second parameter.

## Building and editing (`range`, `slice`, `append`, `insert`, `removeat`)

`range` is the only function that **creates** a series: everything else in the
engine transforms what comes in. The end is **excluded**, and a single argument
counts from zero — so the series lines up with the indices of `skip` and
`slice`.

```jslt
{
  "douze_mois": count(range(1, 13)),
  "page": slice($.l, 1, 3),
  "avec_un_de_plus": append($.l, 9),
  "sans_le_premier": removeat($.l, 0)
}
```

```json
{ "l": [1, 2, 3, 4] }
```

```json
{ "douze_mois": 12, "page": [2, 3], "avec_un_de_plus": [1, 2, 3, 4, 9], "sans_le_premier": [2, 3, 4] }
```

The four edits return a **copy**: a function that modified the input array would
break the other readings of the same document. The bounds are tolerant like
`substring`'s (an over-large index does not raise), while `range` does refuse a
zero step or a series of more than a million elements — it is the only place
where a template can ask for an outsized array.

## Aggregating per group (`groupby`, `countby`, `sumby`, `avgby`)

`group` returns `{ "Label", "Items" }` groups. `groupby(l, key)` returns an
**object** `{ key: elements }`, which `entries` can walk: per-group aggregation
then fits in one expression. `countby` does the most frequent case directly. The
key is converted to text, since a JSON object key is a string.

```jslt
{
  "by_city": countby($.l, $.city),
  "totals": fromentries([
    { "$source": entries(groupby($.l, $.city)),
      "key": $.key,
      "value": sum(selectmany($.value, $.*.m)) }
  ])
}
```

```json
{ "l": [
  { "city": "Lyon", "m": 10 },
  { "city": "Nice", "m": 20 },
  { "city": "Lyon", "m": 5 }
] }
```

```json
{ "by_city": { "Lyon": 2, "Nice": 1 }, "totals": { "Lyon": 15, "Nice": 20 } }
```

`sumby` and `avgby` do that total directly: it is the most frequent use of
grouping, and it took four nested functions. The key is computed per element as
for `sort`; the 3rd argument is the **value** to aggregate, and when it is
omitted the element itself is — so an array of numbers aggregates without it. A
non-numeric value **raises**, as for `sum`: a total that skips the intruders is
plausible and wrong.

A composite key yields a **textual** key (`["FR","Lyon"]`, as compact JSON). To
read it back by path, `groupby` **nests** one level per key when its 3rd argument
is `true`:

```jslt
{
  "totals": sumby($.l, $.country, $.m),
  "by_country": groupby($.l, [$.country, $.city], true)
}
```

```json
{ "l": [
  { "country": "FR", "city": "Lyon", "m": 10 },
  { "country": "FR", "city": "Nice", "m": 20 },
  { "country": "BE", "city": "Gand", "m": 7 }
] }
```

```json
{
  "totals": { "FR": 30, "BE": 7 },
  "by_country": {
    "FR": { "Lyon": [{ "country": "FR", "city": "Lyon", "m": 10 }],
            "Nice": [{ "country": "FR", "city": "Nice", "m": 20 }] },
    "BE": { "Gand": [{ "country": "BE", "city": "Gand", "m": 7 }] }
  }
}
```

Nesting requires an array of keys, and the **same number** of keys for every
element: otherwise one key would carry both elements and a subgroup, and one of
the two would disappear.

---

**See also**: [Conditionals and loops](conditions-et-boucles.en.md) to walk
a collection, [JSONPath paths](chemins.en.md) to filter it.

---

[← jslt guide](guide.en.md)
