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

- [Data and collections](collections.en.md) — `sum`, `distinct`, `limit`, `skip`,
  `union`, `flatten`, `select`, `selectmany`, `zip`, `unzip`, `chunk`, `window`,
  `partition`, `distinctby`, `intersect`, `difference`, `group`, `groupby`,
  `countby`, `sumby`, `avgby`, `join`, `index`, `sort`, `reverse`, `first`,
  `last`, `count`, `avg`, `median`, `product`, `variance`, `stddev`,
  `percentile`, `mode`
- [Objects and deep structures](objets.en.md) — `keys`, `values`, `entries`,
  `fromentries`, `merge`, `pick`, `omit`, `has`, `renamekeys`,
  `flattenobject`, `unflatten`, `walk`, `prune`, `setpath`, `unsetpath`
- [Types, error fallback and validation](types.en.md) — `typeof`, `isarray`,
  `isobject`, `isstring`, `isnumber`, `isboolean`, `trydefault`, `parsejson`,
  `schema`, `schemaerrors`, `schemaisvalid`
- [Numbers and math](nombres.en.md) — `min`, `max`, `abs`, `floor`, `ceil`,
  `round`, `sqrt`, `log`, `parsenumber`, `sign`, `clamp`, `gcd`, `tobase`,
  `isfinite`…
- [Text, regular expressions and formatting](texte.en.md) — `upper`, `split`,
  `splitstring`, `splitregex`, `substring`, `replace`, `regexreplace`, `shorten`,
  `slugify`, `levenshtein`, `similarity`, `foldtext`, `deaccent`, `normalize`,
  `format`
- [Encoding, digests and escaping](encodage.en.md) — `tobase64`, `sha256`,
  `hmacsha256`, `urlencode`, `htmlescape`, `hexencode`…
- [Dates and times](dates.en.md) — `parsedate` (culture, mask, timezone), `dateadd`,
  `datesub`, `datediff`, `datepart`
- [Text output](sortie.en.md) — `to_json`, `to_block`, `to_csv`, `to_xml`,
  `to_yaml`, `$directives.output`
- [Quality: refusing, observing, validating](qualite.en.md) — `require`,
  `requirethat`, `trace`, `traces`, `isemail`, `isurl`, `isuuid`, `isiban`

**Reference**

- [Every function, one page each](fonctions/sommaire.en.md) — signature,
  arguments and description, generated from the registry. That is where the
  editor's tooltip leads; the examples stay in the chapters above.

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

An argument can be **lazy**: the function evaluates it itself, when it wants and
against the source it chooses. That is what lets `sort` compute a key **per
element** and `trydefault` evaluate its fallback only if the first computation
fails. It changes nothing about how a call is written.

> Not every function is illustrated here: trigonometry (`sin`, `cos`…) follows
> the same conventions as the other numeric functions, and `uuid()`, `now()`,
> `today()` are non-deterministic. The authoritative list is
> `default_registry.names()`; the editor and the playground read it directly.

To call the engine from code — including its internal pieces — see
[Embedding the engine](integration.en.md).

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
| External parameter | `param("batch", "default")` | [Expressions](expressions.en.md#external-parameters-param-params) |
| Error fallback | `trydefault(expr, fallback)` | [Types](types.en.md#error-fallback-trydefault) |
| Explicit refusal | `require($.x, "message")` | [Quality](qualite.en.md#refusing-require-requirethat) |
| Observation | `trace($.x, "label")` | [Quality](qualite.en.md#observing-trace-traces) |
| Sorting | `sort($.l, $.k, true)` | [Collections](collections.en.md#sorting-and-ordering-sort-reverse-first-last) |
| Total per group | `sumby($.l, $.k, $.v)` | [Collections](collections.en.md#aggregating-per-group-groupby-countby-sumby-avgby) |

For the internal architecture and the porting choices, see
[`CLAUDE.md`](../CLAUDE.md) (in French).

