# Types, error fallback and validation — jslt guide

*[Français](types.md) · English*

[← jslt guide](guide.en.md) · the examples on this page are **run by the test
suite** (`tests/test_guide_examples.py`) as *template → input → output* triples.

---

## Asking about the type: `typeof` and the predicates

The engine could only say `isnull` / `isnotnull`. A field that is sometimes a
scalar and sometimes a list — an everyday legacy export — was therefore not
tractable.

`typeof(value)` returns the JSON type name: `null`, `boolean`, `number`,
`string`, `array` or `object`; that is JSON Schema's vocabulary, so the same word
works here and in a schema. The predicates `isarray`, `isobject`, `isstring`,
`isnumber` and `isboolean` return a boolean, and are **false** for `null`.

A boolean is **not** a number: `isnumber(true)` is false, as in JSON.

```jslt
{
  "shape": typeof($.value),
  "list": when(isarray($.value)) { "true": $.value, "default": [$.value] }
}
```

```json
{ "value": "alone" }
```

```json
{ "shape": "string", "list": ["alone"] }
```

## Error fallback: `trydefault`

`??` handles the **missing** value. `trydefault(expression, fallback)` handles
the expression that **fails**: division by zero, impossible cast, a function
refusing its data. Both arguments are evaluated lazily — the fallback only when
it is needed, so it may be expensive without penalising the normal case.

Only engine errors (`JsltError`) are caught. A **non-ported** construct
(`NotImplementedError`) passes through: that is a gap in the engine, not faulty
data, and catching it would make it look like an edge case.

```jslt
{
  "ratio": trydefault($.part / $.total, 0),
  "quantity": trydefault($.qty #integer, -1)
}
```

```json
{ "part": 3, "total": 0, "qty": "twelve" }
```

```json
{ "ratio": 0, "quantity": -1 }
```

## Reading JSON held in a string: `parsejson`

`to_json` is an **output** function, refused in the template body: there was no
way back. `parsejson(text)` opens a string that *contains* JSON — a text column
in a database, an encapsulated payload, a stored response. Invalid text
**raises** instead of returning `null`: a corrupted payload yielding an empty
result would be discovered far from its cause. With `trydefault`, the fallback
stays in your hands.

```jslt
{ "city": parsejson($.payload) -> select($.address.city) }
```

```json
{ "payload": "{\"address\":{\"city\":\"Lyon\"}}" }
```

```json
{ "city": "Lyon" }
```

---

## Validating against a schema: `schemaerrors`, `schemaisvalid`

`schema` **infers** a schema from an example; these two do the opposite, they
**confront** a document with a schema. `schemaerrors` returns the list of errors,
each one located (`$.tags[1] : attendu une chaîne, reçu un nombre`);
`schemaisvalid` returns a boolean. Returning the list rather than a bare boolean
is what lets you reject a feed **and say why**.

Keywords checked: `$ref` (internal, into `definitions`), `type` (including
`integer`), `enum`, `properties`, `additionalProperties: false`, `required`,
`items` (single schema or per position), `minItems`, `maxItems`, `uniqueItems`,
`minimum`, `maximum`, `exclusiveMinimum`, `exclusiveMaximum` (both the draft-04
boolean and draft-06 numeric forms), `minLength`, `maxLength`, `pattern`, and the
`format` values `schema` produces (`date`, `date-time`, `duration`).

**Unknown keywords are ignored**, deliberately: `allOf`, `oneOf`, an external
`$ref`… do not cause the schema to be rejected, they are simply not checked.
Raising would make the function unusable on real schemas; the price is that a
document may be declared valid when an unhandled keyword would have rejected it.
This is a **useful** validation, not a **complete** one.

```jslt
{
  "valid": schemaisvalid($.client, $.model),
  "errors": schemaerrors($.client, $.model)
}
```

```json
{
  "model": {
    "type": "object",
    "required": ["name", "age"],
    "properties": { "name": { "type": "string" }, "age": { "type": "integer", "minimum": 0 } }
  },
  "client": { "name": "Ana", "age": -1 }
}
```

```json
{
  "valid": false,
  "errors": ["$.age : minimum 0 non respecté (reçu -1)"]
}
```

The loop closes: what `schema` infers validates the very example it came from.

---

## Schema: `schema`

`schema(sample)` infers a JSON Schema (draft-04) from a JSON fragment, like
nested objects become referenced `definitions`.

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

**See also**: [Objects](objets.en.md) to reshape an object whose form you now
know, [Casts `#type`](expressions.en.md#casts-type) to convert.

---

[← jslt guide](guide.en.md)
