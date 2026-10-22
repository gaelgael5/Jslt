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

1. [Mental model](#1-mental-model)
2. [Constants and structure](#2-constants-and-structure)
3. [JSONPath: reading the source](#3-jsonpath-reading-the-source)
4. [0 / 1 / N semantics](#4-0--1--n-semantics)
5. [Variables](#5-variables)
6. [Operators](#6-operators)
7. [Coalescing `??` and missing values](#7-coalescing--and-missing-values)
8. [Built-in functions](#8-built-in-functions)
9. [Casts `#type`](#9-casts-type)
10. [Chaining `->`](#10-chaining--)
11. [`when` / `switch`](#11-when--switch)
12. [Loops `$source` / `$where`](#12-loops-source--where)
13. [JSONPath filters `?(...)`](#13-jsonpath-filters-)
14. [Path functions `length()` / `value()`](#14-path-functions-length--value)
15. [Re-serialization `to_source()`](#15-re-serialization-to_source)
16. [Extensibility: functions and plugins](#16-extensibility-functions-and-plugins)
17. [Debugging (step-by-step)](#17-debugging-step-by-step)
18. [Errors](#18-errors)
19. [Cheat sheet](#19-cheat-sheet)

---

## 1. Mental model

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

## 2. Constants and structure

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

## 3. JSONPath: reading the source

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

## 4. 0 / 1 / N semantics

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

## 5. Variables

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

## 6. Operators

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

## 7. Coalescing `??` and missing values

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

## 8. Built-in functions

Functions are called by name: `function(arg1, arg2, ...)`. Each argument is an
evaluated expression.

### Core: `sum`, `concat`, `distinct`

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

### Math: `min`, `max`, `abs`, `floor`, `round`…

.NET quirks preserved: `floor`/`round`/`min`/`max` return a **float**, `round`
does **banker's rounding** (0.5 → 0, 1.5 → 2), and `min`/`max` are **binary** (two
arguments).

```jslt
{ "min": min($.a, $.b), "max": max($.a, $.b), "abs": abs($.n), "floor": floor($.d) }
```
```json
{ "a": 2, "b": 8, "n": -5, "d": 2.9 }
```
```json
{ "min": 2.0, "max": 8.0, "abs": 5, "floor": 2.0 }
```

Banker's rounding:

```jslt
{ "demi": round($.x), "trois_demis": round($.y) }
```
```json
{ "x": 0.5, "y": 1.5 }
```
```json
{ "demi": 0.0, "trois_demis": 2.0 }
```

### Text: `upper`, `lower`, `trim`, `split`, `startswith`, `stringcontains`…

```jslt
{ "maj": upper($.s), "parts": split($.s, ",") }
```
```json
{ "s": "a,b,c" }
```
```json
{ "maj": "A,B,C", "parts": ["a", "b", "c"] }
```

```jslt
{ "trim": trim($.s), "debut": startswith($.s, " h"), "contient": stringcontains($.s, "ell") }
```
```json
{ "s": " hello " }
```
```json
{ "trim": "hello", "debut": true, "contient": true }
```

### Regular expressions: `regexismatch`, `regexmatches`

`regexismatch(text, pattern)` tells whether the text contains a match;
`regexmatches(text, pattern)` returns the list of full matches. A number or a
boolean is converted to text first; `null`, an object or an array yield `null`.
Inside a jslt string, backslashes are doubled (`"\\d+"`). The .NET named-group
syntax `(?<name>…)` is accepted.

```jslt
{ "valide": regexismatch($.mail, "^[\\w.]+@[\\w.]+\\.[a-z]+$"), "nombres": regexmatches($.s, "\\d+") }
```
```json
{ "mail": "bob@ex.fr", "s": "lot 12, ref 345" }
```
```json
{ "valide": true, "nombres": ["12", "345"] }
```

### Collection tests: `any`, `contains`, `selectany`

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

### Dates and Unicode: `parsedate`, `normalize`

`parsedate(text, culture)` reads a date (ISO 8601, or numeric by culture:
`fr-FR` day first, `en-US` or empty month first) and returns ISO 8601;
`normalize` composes Unicode characters (form C).

```jslt
{ "fr": parsedate($.d, "fr-FR"), "us": parsedate($.u, "en-US") }
```
```json
{ "d": "22/10/2026 14:05", "u": "10/22/2026" }
```
```json
{ "fr": "2026-10-22T14:05:00", "us": "2026-10-22T00:00:00" }
```

### Collections: `limit`, `union`, `select`, `selectmany`

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

> Other functions are ported (trigonometry, base64 encoding / hashing, `isnull`,
> `uuid`, `now`…). See the full list in [`CLAUDE.md`](../CLAUDE.md) (in French).
> `uuid()` and `now()` are non-deterministic and therefore not illustrated here.

---

## 9. Casts `#type`

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

## 10. Chaining `->`

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

## 11. `when` / `switch`

`when(expr) { "case": block, ..., "default": block }` compares `expr` (`==`) to
each case name and returns the block of the first matching case; otherwise
`default`; otherwise `null`. `switch` is an **alias** of `when`. The comparison
coerces types, so a numeric code matches a textual case name.

```jslt
{ "statut": when($.code) { "200": "ok", "404": "introuvable", "default": "autre" } }
```
```json
{ "code": 404 }
```
```json
{ "statut": "introuvable" }
```

With no matching case and no `default`, the result is `null`:

```jslt
{ "statut": when($.code) { "200": "ok" } }
```
```json
{ "code": 500 }
```
```json
{ "statut": null }
```

---

## 12. Loops `$source` / `$where`

An array containing **one object** with a `"$source"` is a **loop**: the object is
produced for each element of `$source`, and `$` there denotes the **current
element**. `"$where"` filters the elements (keeps only those whose expression is
true).

```jslt
[ { "$source": $.users, "nom": $.name, "majeur": $.age >= 18 } ]
```
```json
{ "users": [ { "name": "A", "age": 30 }, { "name": "B", "age": 15 } ] }
```
```json
[ { "nom": "A", "majeur": true }, { "nom": "B", "majeur": false } ]
```

With `$where` to keep only the active ones:

```jslt
[ { "$source": $.users, "$where": $.actif, "nom": $.name } ]
```
```json
{ "users": [ { "name": "A", "actif": true }, { "name": "B", "actif": false } ] }
```
```json
[ { "nom": "A" } ]
```

---

## 13. JSONPath filters `?(...)`

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

Logical `&` (here a single match → the value, see §4):

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

## 14. Path functions `length()` / `value()`

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

## 15. Re-serialization `to_source()`

`JsltTemplate.to_source()` rebuilds a **valid, re-parseable** template from the AST
(analogous to .NET's `ToString`). The result is equivalent in **behavior** (not
necessarily identical character-for-character); a `#type` cast reappears in its
`convert(x, "type")` form.

```python
from urban_json import JsltTemplate

tpl = JsltTemplate.parse('{ "sum": $.a + $.b }')
tpl.to_source()                          # -> '{ "sum": $.a + $.b }'
JsltTemplate.parse(tpl.to_source())      # re-parseable without error
```

---

## 16. Extensibility: functions and plugins

You can **add** your own functions, **isolate** them, **discover** them, and
consume installed **third-party plugins** — the idiomatic Python equivalent of
.NET's service mechanism.

### Adding a function

```python
from urban_json import jslt_function, JsltTemplate

@jslt_function("double", description="Doubles a number")
def _double(ctx, x=None):
    return x * 2

JsltTemplate.parse('{ "r": double($.n) }').transform({"n": 21})   # -> {'r': 42}
```

A function always receives the execution context as its first parameter (`ctx`),
then the template arguments. `path_args=(indices)` marks arguments received as a
compiled (unevaluated) JSONPath, as for `distinct`.

### Isolating a set of functions

A dedicated registry lets you limit/isolate the available functions (sandbox):

```python
from urban_json import FunctionRegistry, default_registry, JsltTemplate

sandbox = FunctionRegistry()                      # empty: no built-in functions
sandbox.register("triple", lambda ctx, x=None: x * 3)
JsltTemplate.parse('{ "r": triple($.n) }').transform({"n": 7}, functions=sandbox)

# Start from the built-ins without mutating the global registry:
derived = default_registry.copy()
derived.register("triple", lambda ctx, x=None: x * 3)
```

### Discovering available functions

```python
from urban_json import default_registry

default_registry.names()                 # ['abs', 'concat', 'distinct', ...]
info = default_registry.describe("distinct")
info.signature()                         # 'distinct(source, path)'
info.path_args                           # (1,)
info.description                         # first docstring line
info.parameters[1].name, info.parameters[1].type, info.parameters[1].is_path
#                                        # ('path', 'Any', True)
```

To feed a **template editor** (auto-completion, contextual help), `catalog()`
returns a **JSON-serializable** list describing every function (name, description,
parameters name + type + required + path, return type, signature):

```python
import json
from urban_json import default_registry

json.dumps(default_registry.catalog())   # ready to hand to an editor
# [{"name": "distinct", "description": "...", "signature": "distinct(source, path)",
#   "parameters": [{"name": "source", "type": "Any", "required": false, ...},
#                  {"name": "path", "type": "Any", "is_path": true, ...}],
#   "returns": "list", "path_args": [1]}, ...]
```

### Third-party plugins (entry points)

An installed package exposes its functions by declaring the `urban_json.functions` entry
point group. On the plugin side, in its `pyproject.toml`:

```toml
[project.entry-points."urban_json.functions"]
my_package = "my_package.jslt_ext:register"
```

with a `register` function that registers into the given registry:

```python
def register(registry):
    registry.register("shout", lambda ctx, s=None: (s or "").upper() + "!")
```

Plugins are discovered **automatically** on the first `transform` (or on demand via
`load_plugins()`), then usable in templates like the built-in functions. This is
the mechanism intended for the additional packages (I/O: CSV, databases,
Elasticsearch…).

---

## 17. Debugging (step-by-step)

`JsltTemplate.debug(source)` evaluates the template while collecting a
**step-by-step trace**: one step per evaluated node, with its location, the current
source and the produced value. (The engine is an interpreter, so debugging happens
at the template level — there is no generated code as in .NET.)

```python
from urban_json import JsltTemplate

r = JsltTemplate.parse('{ "t": sum($.n) }').debug({"n": [1, 2, 3]})
r.result                      # {'t': 6}
for step in r.steps:
    print(step.kind, step.line, step.expression, "->", step.result)
# JsltPath 1 $.n -> [1, 2, 3]
# JsltFunctionCall 1 sum(…) -> 6
# JsltObject 1 None -> {'t': 6}
```

**Breakpoints**: flag the steps matching a function ("context method") or a template
line.

```python
r = JsltTemplate.parse('{ "t": sum($.n) }').debug({"n": [1, 2]}, break_functions=["sum"])
[s.expression for s in r.steps if s.breakpoint]   # ['sum(…)']
```

`DebugResult` carries `result` (final value), `steps` (list of `TraceStep`) and
`error` (message if evaluation fails — the partial trace is still available). The
playground (`apps/playground`) offers a visual step-through.

---

## 18. Errors

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

## 19. Cheat sheet

| Construct | Syntax | Section |
|---|---|---|
| Path | `$.a.b`, `$.l[0]`, `$.l[1:3]`, `$.*`, `$..k` | [3](#3-jsonpath-reading-the-source) |
| Variable | `"v:": expr`, `v:`, `v:$.x` | [5](#5-variables) |
| Arithmetic | `+ - * / %` | [6](#6-operators) |
| Comparison | `== != < <= > >=` | [6](#6-operators) |
| Boolean logic | `&& \|\| !` | [6](#6-operators) |
| Bitwise / XOR | `& \| ^` | [6](#6-operators) |
| Coalescing | `a ?? b` | [7](#7-coalescing--and-missing-values) |
| Function | `f(a, b)` | [8](#8-built-in-functions) |
| Cast | `expr #integer` | [9](#9-casts-type) |
| Chaining | `expr -> f()` | [10](#10-chaining--) |
| Conditional | `when(e) { "c": v, "default": d }` | [11](#11-when--switch) |
| Loop | `[ { "$source": $.l, "$where": c, ... } ]` | [12](#12-loops-source--where) |
| Filter | `$.l[?(@.x > 1 & @.y in [..])]` | [13](#13-jsonpath-filters-) |
| Path function | `$.x.length()`, `$.x.value()` | [14](#14-path-functions-length--value) |

For the internal architecture, the porting patterns and the deliberate deviations
from .NET, see [`CLAUDE.md`](../CLAUDE.md) (in French).
