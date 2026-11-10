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

## Schema: `schema`

`schema(sample)` infers a JSON Schema (draft-04) from a JSON fragment, like
NJsonSchema on the .NET side: nested objects become referenced `definitions`.

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

**See also**: [Conditionals and loops](conditions-et-boucles.en.md) to walk
a collection, [JSONPath paths](chemins.en.md) to filter it.

---

[← jslt guide](guide.en.md)
