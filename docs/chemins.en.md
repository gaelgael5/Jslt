# JSONPath paths — jslt guide

*[Français](chemins.md) · English*

[← jslt guide](guide.en.md) · the examples on this page are **run by the test
suite** (`tests/test_guide_examples.py`) as *template → input → output* triples.

---

## Reading the source

`$` is the root of the source document. You navigate with `.key`, `[index]`,
`[start:end]` (slice), `*` (wildcard) and `..` (recursive descent).

### Access by key

```jslt
{ "nom": $.user.name, "age": $.user.age }
```
```json
{ "user": { "name": "Alice", "age": 30 } }
```
```json
{ "nom": "Alice", "age": 30 }
```

### Index, slice, wildcard

```jslt
{ "premier": $.items[0], "slice": $.items[1:3], "wild": $.obj.* }
```
```json
{ "items": [10, 20, 30, 40], "obj": { "x": 1, "y": 2 } }
```
```json
{ "premier": 10, "slice": [20, 30], "wild": [1, 2] }
```

### Recursive descent `..`

`$..id` collects **all** `id`s, at any depth, in document traversal order (a node
is inspected before its children):

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

## 0 / 1 / N semantics

A path (or a filter) may select **0, 1 or N** values. The result follows the .NET
engine rule (`GetContentByJPath`):

| Matches | Result |
|---|---|
| 0 | `null` |
| 1 | the value (not a single-element list) |
| N | the list of values |

Zero matches → `null`:

```jslt
{ "r": $.inconnu }
```
```json
{ "a": 1 }
```
```json
{ "r": null }
```

A single match → the value directly:

```jslt
{ "r": $.items[?(@.n == 2)] }
```
```json
{ "items": [ { "n": 1 }, { "n": 2 }, { "n": 3 } ] }
```
```json
{ "r": { "n": 2 } }
```

Several matches → a list:

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

## JSONPath filters `?(...)`

`$.items[?(cond)]` keeps only the elements satisfying `cond`. In the condition,
`@` denotes the current element and `$` the root of the document. Operators:
comparisons `== != < <= > >=`, logical `&` (and) / `|` (or), membership `in`.

```jslt
{ "grands": $.items[?(@.n > 1)] }
```
```json
{ "items": [ { "n": 1 }, { "n": 2 }, { "n": 3 } ] }
```
```json
{ "grands": [ { "n": 2 }, { "n": 3 } ] }
```

Logical `&` (here a single match → the value, see [0 / 1 / N semantics](#0--1--n-semantics)):

```jslt
{ "r": $.items[?(@.ok == true & @.n > 1)] }
```
```json
{ "items": [ { "n": 1, "ok": true }, { "n": 3, "ok": true } ] }
```
```json
{ "r": { "n": 3, "ok": true } }
```

Membership `in` with a literal or a path:

```jslt
{ "autorises": $.items[?(@.id in [2, 3])] }
```
```json
{ "items": [ { "id": 1 }, { "id": 2 }, { "id": 3 } ] }
```
```json
{ "autorises": [ { "id": 2 }, { "id": 3 } ] }
```

Comparison against a value from the root:

```jslt
{ "r": $.items[?(@.n >= $.seuil)] }
```
```json
{ "items": [ { "n": 1 }, { "n": 2 }, { "n": 3 } ], "seuil": 2 }
```
```json
{ "r": [ { "n": 2 }, { "n": 3 } ] }
```

A filter commonly feeds a loop:

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

## Path functions `length()` / `value()`

At the end of a path, `length()` gives the size (array, object or string; `null`
for a non-measurable scalar) and `value()` returns the value as-is. Also usable in
filters.

```jslt
{ "taille": $.tags.length(), "valeur": $.v.value() }
```
```json
{ "tags": ["a", "b", "c"], "v": 42 }
```
```json
{ "taille": 3, "valeur": 42 }
```

In a filter:

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

[← jslt guide](guide.en.md)
