# Quality: refusing, observing, validating — jslt guide

*[Français](qualite.md) · English*

[← jslt guide](guide.en.md) · the examples on this page are **run by the test
suite** (`tests/test_guide_examples.py`) as *template → input → output* triples.

---

Two things were missing for a template to be viable in production: being able to
**refuse** data, and being able to **look** at what it does.

## Refusing: `require`, `requirethat`

Without them, a template facing unacceptable data had only two ways out:
producing a wrong output, or triggering an error by accident (a well-placed
division by zero). The refusal is now explicit and carries a **business
message**.

- `require(value, message)` returns the value if it is **present**, otherwise
  raises. Only absence (`null`) is refused: `0`, `false`, `""` and `[]` are
  values, and refusing them would make the function unusable on a zero amount.
- `requirethat(condition, message)` requires a **strictly** true condition. A
  condition worth `0` or `""` is nearly always an expression you believed to be
  boolean: letting it pass for false would hide the authoring mistake.

Both raise a `JsltError`, hence in the same family as the rest of the engine:
`trydefault` can catch them when the refusal should stay local.

```jslt
{
  "id": require($.id, "client id is required"),
  "discount": trydefault(require($.discount, "missing"), 0)
}
```

```json
{ "id": "C-12" }
```

```json
{ "id": "C-12", "discount": 0 }
```

## Observing: `trace`, `traces`

Step-by-step exists at API level (`JsltTemplate.debug`), not at language level:
there was no way to look at an intermediate value without adding it to the
result, hence without changing what you measure.

`trace(value, label)` returns the value **unchanged** and records it. `traces()`
returns the current run's journal, which the template can put wherever it wants —
or nowhere, an integrator then reading it from the context (`context.traces`, see
[Embedding the engine](integration.en.md)).

The journal lives on the execution context: two runs, even concurrent ones, never
see each other's traces.

```jslt
{
  "total": trace($.a, "a") + trace($.b, "b"),
  "_diagnostic": traces()
}
```

```json
{ "a": 2, "b": 3 }
```

```json
{
  "total": 5,
  "_diagnostic": [ { "label": "a", "value": 2 }, { "label": "b", "value": 3 } ]
}
```

## Validating a format: `isemail`, `isurl`, `isuuid`, `isiban`

Four predicates, deliberately **pragmatic**. An address conforming to the full
RFC 5322 accepts forms nobody uses (comments, quoted strings): a validator that
accepts them lets through what a downstream system will reject.

`isiban` checks the structure **and** the check digits (modulo 97), which catch
typos. The per-country expected length is not checked: that would be a table of
over sixty entries to maintain, and its going stale would reject a valid IBAN — a
false rejection costs more here than a false acceptance, which the bank will
reject anyway.

These predicates return a **boolean**: `null` and a number are not valid
addresses, and returning `null` would force the caller to tell three cases apart
where the question is closed.

```jslt
{
  "mail": requirethat(isemail($.mail), "invalid email address"),
  "iban_ok": isiban($.iban)
}
```

```json
{ "mail": "a.b@example.com", "iban": "FR1420041010050500013M02606" }
```

```json
{ "mail": true, "iban_ok": true }
```

---

**See also**: [Types and validation](types.en.md) to validate a whole **shape**
against a JSON Schema, [Embedding the engine](integration.en.md) to read the
traces from the calling code.

---

[← jslt guide](guide.en.md)
