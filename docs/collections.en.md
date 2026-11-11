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
JSONPath (written as a string, as in .NET, or directly) selects at least one
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
(so "Zoé" before "école"), arrays and objects by their compact JSON — arbitrary
but stable. For a human order, sort on a folded key (`foldtext`). The sort is
**stable** both ways: equal keys keep their original order.

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

An element whose key is missing counts as `null`, so it comes **first**: gaps
gather where you can see them, instead of making the sort raise.

## Aggregating (`count`, `avg`, `median`, `product`, `min`, `max`)

`sum` was alone, and `min`/`max` were **binary** (two numbers): "the smallest in
the list" did not exist. `min` and `max` now accept **an array** in addition to
their two-argument .NET form — it is the same question, and `sum($.n)` already
aggregates. Given an array they preserve the type (an integer stays an integer);
given two numbers they keep the .NET quirk of a decimal result. Passing an array
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

**See also**: [Conditionals and loops](conditions-et-boucles.en.md) to walk
a collection, [JSONPath paths](chemins.en.md) to filter it.

---

[← jslt guide](guide.en.md)
