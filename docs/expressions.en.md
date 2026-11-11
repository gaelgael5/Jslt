# Expressions: variables, operators, casts — jslt guide

*[Français](expressions.md) · English*

[← jslt guide](guide.en.md) · the examples on this page are **run by the test
suite** (`tests/test_guide_examples.py`) as *template → input → output* triples.

---

## Variables

A variable **declaration** is a key ending in `:` (e.g. `"u:"`). Its value is
evaluated once, then reusable by **reference** `name:` or by **projection**
`name:$.path` (the path is then applied *to the variable*). Declaration keys do
not appear in the output.

```jslt
{ "u:": $.user, "nom": u:$.name, "ville": u:$.city }
```
```json
{ "user": { "name": "Bob", "city": "Lyon" } }
```
```json
{ "nom": "Bob", "ville": "Lyon" }
```

Plain reference (no projection):

```jslt
{ "v:": 42, "copie": v: }
```
```json
{}
```
```json
{ "copie": 42 }
```

---

## Operators

### Arithmetic `+ - * / %`

**Integer** division truncates toward zero (C# behavior); as soon as one operand
is decimal, division is real.

```jslt
{ "add": $.a + $.b, "sub": $.a - $.b, "mul": $.a * $.b, "div": $.a / $.b, "mod": $.a % $.b }
```
```json
{ "a": 17, "b": 5 }
```
```json
{ "add": 22, "sub": 12, "mul": 85, "div": 3, "mod": 2 }
```

```jslt
{ "div_reelle": $.a / $.b }
```
```json
{ "a": 17.0, "b": 5 }
```
```json
{ "div_reelle": 3.4 }
```

### Comparison `== != < <= > >=`

```jslt
{ "eq": $.a == $.b, "lt": $.a < $.b, "ge": $.a >= $.b }
```
```json
{ "a": 3, "b": 4 }
```
```json
{ "eq": false, "lt": true, "ge": false }
```

### Boolean logic `&& || !`

```jslt
{ "et": $.x && $.y, "ou": $.x || $.y, "non": !$.x }
```
```json
{ "x": true, "y": false }
```
```json
{ "et": false, "ou": true, "non": false }
```

### Bitwise `&` `|` and XOR `^`

Note: faithfully to .NET, `&`/`|` are the **integer bitwise** operators (not
boolean — those are `&&`/`||`), and `^` is **integer XOR**.

```jslt
{ "bitand": $.a & $.b, "bitor": $.a | $.b, "xor": $.a ^ $.b }
```
```json
{ "a": 6, "b": 3 }
```
```json
{ "bitand": 2, "bitor": 7, "xor": 5 }
```

---

## Coalescing `??` and missing values

`a ?? b` returns `a` if it is not `null`, otherwise `b`. Combined with the "0
matches → null" semantics, this is the idiomatic way to give a default value to an
absent field.

```jslt
{ "ville": $.user.city ?? "inconnue" }
```
```json
{ "user": { "name": "Z" } }
```
```json
{ "ville": "inconnue" }
```

If the value exists, it wins:

```jslt
{ "ville": $.user.city ?? "inconnue" }
```
```json
{ "user": { "city": "Nantes" } }
```
```json
{ "ville": "Nantes" }
```

---

## Casts `#type`

A `#type` suffix converts the value. Fully supported types: `#integer`,
`#decimal`, `#string`, `#boolean`.

```jslt
{ "i": $.s #integer, "d": $.s2 #decimal, "str": $.n #string, "b": $.s3 #boolean }
```
```json
{ "s": "42", "s2": "3.14", "n": 42, "s3": "true" }
```
```json
{ "i": 42, "d": 3.14, "str": "42", "b": true }
```

> A cast `x #type` is equivalent to `convert(x, "type")`; that is in fact the form
> it is re-serialized to by `to_source()`.

---

## Chaining `->`

`a -> f()` passes `a` as the first argument to `f`: `$.n -> sum()` is equivalent to
`sum($.n)`. Handy for left-to-right reading.

```jslt
{ "total": $.n -> sum() }
```
```json
{ "n": [1, 2, 3] }
```
```json
{ "total": 6 }
```

---

## External parameters (`param`, `params`)

`transform(source)` only took the document: a template could receive "the
reference date" or "the batch id" only by injecting them into the source, which
mixes the **data** being transformed with the **settings** of the run.

```python
template.transform(document, parameters={"batch": "A-12", "threshold": 100})
```

`param("name")` reads a parameter, `param("name", fallback)` provides a backup
value, `params()` returns the whole object (handy to trace the batch in the
output). A parameter **supplied as `null`** stays `null`: the fallback only
applies to a *missing* parameter, otherwise you could not explicitly pass "no
value".

Parameters are **not** visible to JSONPath: `$.batch` does not reach them. That
is deliberate — a setting is not part of the document, and mixing them would make
a template depend on how it is called.

```jslt
{ "batch": param("batch", "none"), "settings": params() }
```

```json
{ "x": 1 }
```

```json
{ "batch": "none", "settings": {} }
```

(With no parameters the fallback applies and `params()` is empty — which is what
the example above, run without `parameters=`, shows.)

What does **not** exist: defining a function inside the template (no lambda, no
macro, no recursion) and including another template. Both require new syntax,
hence a change to the ANTLR grammar and its regeneration; they cannot be worked
around with a function.

---

[← jslt guide](guide.en.md)
