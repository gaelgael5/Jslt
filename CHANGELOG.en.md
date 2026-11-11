# Changelog

*[Français](CHANGELOG.md) · English*

This log covers the **core** (`urban-json`) and the repository's `urban-json-*`
packages. It also records movements in the **documented internals**
(`urban_json.parsing`, `runtime`, `ast`, `jsonpath`): they are not frozen, but an
integration hooked into them must be able to read here what moved rather than
comparing two versions line by line. The three levels of guarantee are described
in [Embedding the engine](docs/integration.en.md).

Versions follow [SemVer](https://semver.org/); a PyPI version is immutable, so a
documentation fix aimed at the index is worth a patch release.

## urban-json 0.4.0 — 2026-11-11

Fills in eleven missing families of functions. **No breaking change**: nothing is
removed or renamed, existing signatures gain optional arguments.

### Added — 60 functions (75 → 135)

- **Strings**: `substring`, `replace`, `regexreplace`, `trimstart`, `trimend`,
  `repeat`, `titlecase`.
- **Unicode**: `deaccent`, `foldtext` (comparison key: case and/or accents).
- **Sorting and ordering**: `sort` (key computed per element, documented total
  order, stable sort), `reverse`, `first`, `last`.
- **Aggregates**: `count`, `avg`, `median`, `product`.
- **Objects**: `keys`, `values`, `entries`, `fromentries`, `merge`, `pick`,
  `omit`, `has`, `renamekeys`.
- **Types**: `typeof`, `isarray`, `isobject`, `isstring`, `isnumber`,
  `isboolean`.
- **Error fallback**: `trydefault` (evaluates its fallback only if the
  expression raises, and does **not** catch `NotImplementedError`).
- **Validation**: `schemaerrors`, `schemaisvalid` (documented JSON Schema
  subset; unknown keywords are ignored, not rejected).
- **Reading JSON**: `parsejson`.
- **Numbers**: `parsenumber` (the cultures of `format`), `sign`, `clamp`, `gcd`,
  `shiftleft`, `shiftright`, `tohex`, `fromhex`.
- **Dates**: `datestartof`, `dateendof`, `datezone`, `today`, `dateduration`.
- **Encoding and digests**: `md5`, `sha1`, `hmacsha256`, `urlencode`,
  `urldecode`, `htmlescape`, `htmlunescape`, `hexencode`, `hexdecode`.
- **External parameters**: `param`, `params`.

### Changed — widened, compatible signatures

- `min(array)` / `max(array)` aggregate, in addition to their binary .NET form
  (which keeps its decimal result). An array **and** a second argument raises,
  rather than ignoring the second.
- `round(v, digits)`: optional precision, banker's rounding preserved.
- `normalize(v, form)`: `C` (default), `D`, `KC`, `KD`.
- `datepart`: new parts `quarter`, `week` (ISO), `dayofyear`, `millisecond`.
- `dateadd` / `datesub` / `datediff`: new `weekday` unit (business days,
  Monday-Friday, with **no** public-holiday calendar).

### Changed — behaviour

- **Computation errors are now `JsltError`.** A division by zero came out as
  `ZeroDivisionError`, a `+` on text as `ValueError`: unreadable in a message and
  impossible to catch from a template. They remain exceptions, but of the
  engine's family. A caller catching `ZeroDivisionError` or `ValueError`
  **specifically** must switch to `JsltError`; catching `Exception` is
  unaffected.
- **The compiled path and the interpreter no longer diverge on errors.** The
  compiler pre-resolves operators and called the raw callable: the same division
  by zero raised a `ZeroDivisionError` when compiled and a `JsltError` when
  interpreted. The wrapper moved into the operator table, which both paths share.

### Added — API

- `transform(source, functions=…, parameters=…)`, likewise `render` and `debug`:
  external settings read by `param("name")`. They are **not** visible to
  JSONPath.
- `FunctionRegistry.remove(name)`: the counterpart of `register`, to derive a
  restricted registry without rebuilding it.
- `@jslt_function(..., lazy_args=(…))` and `FunctionRegistry.lazy_args_of`:
  arguments received unevaluated, which the function calls when it chooses (the
  mechanism behind `sort` and `trydefault`). The catalog exposes `lazy_args`.

### Documented internals

- `urban_json.parsing` now exports `ScriptBuilderVisitor` (it was only reachable
  through its module). `parse_to_tree` is unchanged.
- `RuntimeContext(sources, functions, parameters)`: **third argument added**,
  optional and positional — an existing two-argument call stays valid.
- `ast`, `jsonpath`: unchanged.

### Documentation

- Guide split by theme (10 → 13 documents per language); three new ones:
  [Objects](docs/objets.en.md), [Types and validation](docs/types.en.md),
  [Encoding](docs/encodage.en.md) — the last one also documents `tobase64`,
  `crc32`, `sha256` and `sha512`, which were documented nowhere.
- [Embedding the engine](docs/integration.en.md): the three surfaces and their
  guarantee, the pipeline piece by piece, and how to restrict functions.
- This log, which did not exist.

### Plugins

- `urban-json-xml 0.2.0`: `parsexml(text)` — `loadxml`'s conversion, from a
  string.
- `urban-json-csv 0.2.0`: `parsecsv(text, …)` — `loadcsv`'s reading, from a
  string, same options.
- Both raise `JsltError` (the engine's family, catchable by `trydefault`), where
  the older file-reading functions keep `ValueError`. The discrepancy is known;
  unifying it would be a breaking change, deferred to a major version.

### Not addressed, and why

- **Functions defined inside the template** (lambda, macro, recursion) and
  **including another template**: they need new syntax, hence a change to the
  ANTLR grammar and its regeneration (Java required). No function works around
  them.
- **YAML**: would require one more dependency and distribution
  (`urban-json-yaml`); that is a scope decision, not an oversight.
- **Locale collation sorting** and **transliteration**: they need ICU. In the
  meantime, sorting on a `foldtext` key gives a human order for languages with
  Latin diacritics.

## urban-json 0.3.0 — 2026-11-10

Documented after the fact: this log did not exist, and the tag announcement said
"no breaking change" without detail.

### Added

- `parsedate(text, culture, mask, timezone)`: 3rd **mask** argument (strict
  reading using `format`'s .NET vocabulary) and 4th **timezone** argument (IANA
  name, `UTC`/`Z`, fixed offset; it assigns to a naive date, converts an
  offset-aware one).
- `dateadd`, `datesub`, `datediff`, `datepart` (71 → 75 functions).

### Changed — behaviour of existing functions

Three changes the announcement did not mention:

- **`parsedate` was entirely rewritten.** A component missing from the mask
  defaults to the Unix epoch, not "today" as in .NET: a template's result must
  not depend on the day it runs.
- **`format` now reads an ISO string suffixed with `Z`** as a date. It used to
  come out raw: an output can therefore **change silently** in that precise case.
- **`format` writes the offset tokens `z`, `zz`, `zzz`, `K`**, which used to
  raise. On a date without an offset, `z` writes zero — .NET would take the
  machine's, and an output must not depend on the server.

### Internals

`parsing/`, `ast/`, `runtime/`, `jsonpath/` and `serialization.py` are
**identical to 0.2.1**. Only five files under `functions/` change. That is what
allowed the upgrade without re-reading every visitor — and precisely what an
integration had had to establish by itself, by comparing sources.

## Before 0.3.0

No log. The git history is authoritative; the published milestones are
`urban-json` 0.1.0, 0.2.0 and 0.2.1, and `urban-json-editor` 0.1.1 → 0.3.0.
