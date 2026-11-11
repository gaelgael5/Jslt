# Objects: keys, values and reshaping — jslt guide

*[Français](objets.md) · English*

[← jslt guide](guide.en.md) · the examples on this page are **run by the test
suite** (`tests/test_guide_examples.py`) as *template → input → output* triples.

---

A template builds its objects **key by key**, literally. As soon as the keys are
only known at run time — a price dictionary, variable columns, an object to be
filtered — they have to be handled as data: that is what these functions do.

| Function | Purpose |
|---|---|
| `keys(object)` | its keys, in document order |
| `values(object)` | its values, in the same order |
| `entries(object)` | `[{ "key": …, "value": … }]` |
| `fromentries(array)` | the inverse: rebuilds the object |
| `merge(a, b, deep)` | merges, the **right side wins** shared keys |
| `pick(object, keys)` | sub-object limited to the requested keys |
| `omit(object, keys)` | object without those keys |
| `has(object, key)` | the key is **present**, even when `null` |
| `renamekeys(object, mapping)` | renames according to `{ old: new }` |

**Conventions.** `null` and any value that is not an object yield `null` — an
array is not "an object without keys", and returning `{}` would suggest an empty
object. `pick` and `omit` accept a single key (`pick($.o, "a")`) or an array; a
requested key that is missing is simply absent from the result, with no error,
because heterogeneous documents are exactly what they are for. None of these
functions modifies its input.

**`has` versus `isnull`.** `isnull($.o.a)` is true for a missing key *as well as*
for a key present with a `null` value. When that distinction matters — field left
blank versus field absent from the feed — `has` is the one you need.

```jslt
{
  "keys": keys($.client),
  "without_internal": omit($.client, ["internal", "trace"]),
  "has_mail": has($.client, "mail"),
  "mail_empty": isnull($.client.mail)
}
```

```json
{ "client": { "name": "Ana", "mail": null, "internal": true, "trace": "x" } }
```

```json
{
  "keys": ["name", "mail", "internal", "trace"],
  "without_internal": { "name": "Ana", "mail": null },
  "has_mail": true,
  "mail_empty": true
}
```

**Merging.** `merge` is **flat** by default: a shared key is replaced, even when
its value is an object. Passing `true` as the third argument descends into
sub-objects.

```jslt
{
  "flat": merge($.defaults, $.client),
  "deep": merge($.defaults, $.client, true)
}
```

```json
{
  "defaults": { "options": { "lang": "en", "theme": "light" } },
  "client": { "options": { "theme": "dark" } }
}
```

```json
{
  "flat": { "options": { "theme": "dark" } },
  "deep": { "options": { "lang": "en", "theme": "dark" } }
}
```

**Walking an object.** `entries` returns named objects — `$.key` and `$.value`
read naturally in a loop, whereas `[key, value]` pairs would force index access,
which says nothing to the next reader. Together with `fromentries`, the round
trip lets you transform the keys themselves.

```jslt
{
  "inverted": fromentries([
    { "$source": entries($.prices), "key": $.value #string, "value": $.key }
  ])
}
```

```json
{ "prices": { "small": 10, "large": 20 } }
```

```json
{ "inverted": { "10": "small", "20": "large" } }
```

**Renaming.** `renamekeys` leaves keys absent from the mapping untouched. On a
collision (renaming `a` to `b` while `b` exists), the **last write wins**, in
document order: raising would be stricter but would make renaming unusable on a
feed that carries both names during a migration.

```jslt
{ "normalised": renamekeys($.line, { "lbl": "label", "qty": "quantity" }) }
```

```json
{ "line": { "lbl": "Screw", "qty": 12, "price": 3 } }
```

```json
{ "normalised": { "label": "Screw", "quantity": 12, "price": 3 } }
```

---

## Deep structures

Reading deep was already possible (`$..k`); **transforming** deep was missing.

| Function | Purpose |
|---|---|
| `flattenobject(o, separator)` | nested object → dotted keys (`addr.city`), arrays indexed |
| `unflatten(o, separator, arrays)` | the inverse; `arrays` set to `true` to read indices back |
| `walk(v, expression)` | applies an expression to **every node**, leaves first |
| `prune(v, options)` | recursively removes `null`, and emptiness with `"empty"` |
| `setpath(o, path, value)` | copy with a value set at the end of a path |
| `unsetpath(o, path)` | copy without that path |

**Flattening.** This is the bridge to a tabular format, and `to_csv` uses it. An
**empty** container is kept as a leaf (`{"a": {}}` stays `{"a": {}}`), otherwise
the round trip would lose information.

**Rebuilding.** Numeric segments only become arrays when asked: a key `2026` is a
year's name in plenty of documents, and turning it into an index would create an
array with two thousand holes. A path that contradicts another (`a` being 1
**and** `a.b` being 2) **raises**: overwriting silently would make data vanish.

```jslt
{
  "flat": flattenobject($.client),
  "back": unflatten(flattenobject($.client), ".", true)
}
```

```json
{ "client": { "id": 1, "addr": { "city": "Lyon" }, "tags": ["a", "b"] } }
```

```json
{
  "flat": { "id": 1, "addr.city": "Lyon", "tags.0": "a", "tags.1": "b" },
  "back": { "id": 1, "addr": { "city": "Lyon" }, "tags": ["a", "b"] }
}
```

**Walking.** `walk` works **from the leaves up**: the expression sees children
that are already transformed, so a rule that depends on them works. The other way
round it would see the original and have to descend by itself.

`prune` removes only `null` by default: an empty string, an empty array and `0`
are **values**, and removing them outright would make an "amount: 0" that says
something disappear. The `"empty"` option is there for the opposite — it keeps
`0` and `false`, which are not empty.

```jslt
{
  "clean": prune($.doc),
  "trimmed": walk($.doc, when(isstring($)) { "true": trim($), "default": $ })
}
```

```json
{ "doc": { "a": " x ", "b": null, "l": [" y ", null] } }
```

```json
{
  "clean": { "a": " x ", "l": [" y "] },
  "trimmed": { "a": "x", "b": null, "l": ["y", null] }
}
```

**Setting and removing.** `setpath` creates the missing levels and walks arrays by
index (`l.1.v`); it **raises** if it would have to overwrite a scalar to descend.
`unsetpath` does not raise on a missing path: you asked for a document without
that data, and it already is. Neither modifies its source.

```jslt
{ "r": setpath($.o, "addr.country", "FR") -> unsetpath("internal") }
```

```json
{ "o": { "addr": { "city": "Lyon" }, "internal": true } }
```

```json
{ "r": { "addr": { "city": "Lyon", "country": "FR" } } }
```

Finally, `merge` takes a 4th argument: `merge(a, b, true, true)` **concatenates**
arrays instead of replacing them. Replacement stays the default, because merging
two lists of different lengths has no single meaning.

---

**See also**: [Types and validation](types.en.md) to find out *whether* a value
is an object, [Data and collections](collections.en.md) for arrays.

---

[← jslt guide](guide.en.md)
