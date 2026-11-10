# jslt guide — JSON → JSON transformation language

*[Français](guide.md) · English*

This guide walks through **every construct of the language** with examples. All
examples are **executed by the test suite** (`tests/test_guide_examples.py`) as
*template → input → output* triples, so they are always correct and up to date.

To reproduce them:

```python
from urban_json import JsltTemplate
JsltTemplate.parse(TEMPLATE).transform(INPUT)   # == OUTPUT
```

> **Reading convention.** In each example, the first block is the jslt
> **template**, the second the **input** (source JSON document), the third the
> expected **output**.

---

## Table of contents

**The language**

- [Mental model](#mental-model) · [Constants and structure](#constants-and-structure)
- [JSONPath paths](chemins.en.md) — access by key, index, slice,
  wildcard, recursive descent `..`, 0 / 1 / N semantics, filters `?(...)`,
  `length()` / `value()`
- [Expressions](expressions.en.md) — variables, operators, coalescing `??`,
  casts `#type`, chaining `->`
- [Conditionals and loops](conditions-et-boucles.en.md) — `when` / `switch`,
  `$source` / `$where`

**Built-in functions** — how they are called:
[Built-in functions](#built-in-functions)

- [Data and collections](collections.en.md) — `sum`, `concat`, `distinct`, `limit`,
  `union`, `select`, `selectmany`, `any`, `contains`, `group`, `join`, `index`, `schema`
- [Numbers and math](nombres.en.md) — `min`, `max`, `abs`, `floor`, `round`, `sqrt`…
- [Text, regular expressions and formatting](texte.en.md) — `upper`, `split`,
  `startswith`, `regexismatch`, `regexmatches`, `normalize`, `format`
- [Dates and times](dates.en.md) — `parsedate` (culture, mask, timezone), `dateadd`,
  `datesub`, `datediff`, `datepart`
- [Text output](sortie.en.md) — `to_json`, `to_block`, `$directives.output`

**Around the language**

- [Extensibility, debugging and re-serialization](extensibilite.en.md) — function
  registry, entry-point plugins, step-by-step, `to_source()`
- [Errors](#errors) · [Cheat sheet](#cheat-sheet)

---

## Mental model

A jslt template **looks like** JSON, but the *values* are **expressions**
evaluated against the source document. The root of the source document is denoted
by `$`.

- The template's **structure** (objects, arrays, keys) describes the shape of the
  output.
- The **values** (`$.x`, `sum(...)`, `$.a + $.b`…) are computed.

A literal value is copied as-is:

```jslt
{ "ville": "Paris", "pays": "FR" }
```
```json
{}
```
```json
{ "ville": "Paris", "pays": "FR" }
```

---

## Constants and structure

The four JSON scalar types are direct constants:

```jslt
{ "i": 6, "d": 6.7, "b": true, "z": null }
```
```json
{}
```
```json
{ "i": 6, "d": 6.7, "b": true, "z": null }
```

Objects and arrays nest freely:

```jslt
{ "meta": { "actif": true }, "codes": [1, 2, 3] }
```
```json
{}
```
```json
{ "meta": { "actif": true }, "codes": [1, 2, 3] }
```

---

## Built-in functions

Functions are called by name: `function(arg1, arg2, ...)`. Each argument is an
evaluated expression.

> Other functions are ported (trigonometry, base64 encoding / hashing, `isnull`,
> `uuid`, `now`…). See the full list in [`CLAUDE.md`](../CLAUDE.md) (in French).
> `uuid()` and `now()` are non-deterministic and therefore not illustrated here.

---

## Errors

A syntactically invalid template raises `JsltSyntaxError` (with line/column):

```python
from urban_json import JsltTemplate, JsltSyntaxError

try:
    JsltTemplate.parse('{ "n": ~ }')
except JsltSyntaxError as e:
    print(e.line, e.column)   # error position
```

A construct recognized by the grammar but **not ported** (e.g. the `contains`
filter operator, the `size()` path function) raises `NotImplementedError` with an
explicit message — never a wrong result:

```python
from urban_json import JsltTemplate

JsltTemplate.parse('{ "r": $.a[?(@.x contains 1)] }')   # -> NotImplementedError
```

---

## Cheat sheet

| Construct | Syntax | Section |
|---|---|---|
| Path | `$.a.b`, `$.l[0]`, `$.l[1:3]`, `$.*`, `$..k` | [Paths](chemins.en.md#reading-the-source) |
| Variable | `"v:": expr`, `v:`, `v:$.x` | [Expressions](expressions.en.md#variables) |
| Arithmetic | `+ - * / %` | [Expressions](expressions.en.md#operators) |
| Comparison | `== != < <= > >=` | [Expressions](expressions.en.md#operators) |
| Boolean logic | `&& \|\| !` | [Expressions](expressions.en.md#operators) |
| Bitwise / XOR | `& \| ^` | [Expressions](expressions.en.md#operators) |
| Coalescing | `a ?? b` | [Expressions](expressions.en.md#coalescing--and-missing-values) |
| Function | `f(a, b)` | [Functions](#built-in-functions) |
| Cast | `expr #integer` | [Expressions](expressions.en.md#casts-type) |
| Chaining | `expr -> f()` | [Expressions](expressions.en.md#chaining--) |
| Conditional | `when(e) { "c": v, "default": d }` | [Loops](conditions-et-boucles.en.md#when--switch) |
| Loop | `[ { "$source": $.l, "$where": c, ... } ]` | [Loops](conditions-et-boucles.en.md#loops-source--where) |
| Filter | `$.l[?(@.x > 1 & @.y in [..])]` | [Paths](chemins.en.md#jsonpath-filters-) |
| Path function | `$.x.length()`, `$.x.value()` | [Paths](chemins.en.md#path-functions-length--value) |

For the internal architecture, the porting patterns and the deliberate deviations
from .NET, see [`CLAUDE.md`](../CLAUDE.md) (in French).

