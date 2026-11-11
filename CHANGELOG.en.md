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

## urban-json-editor 0.4.0 — 2026-11-11

### Added

- **Signature help.** From the opening parenthesis on, the call surrounding the
  caret is recalled with the **parameter being typed in bold**, and it follows
  the commas — the completion list, by contrast, vanished at the first comma and
  never said *where* you were. The commas of an array or an object do not
  advance the parameter (`sort($.l, [$.a, $.b], …)` stays on the 2nd), and an
  extra argument bolds nothing rather than pointing at a random parameter.
- **The help follows the caret, not the typing**: clicking inside the
  parentheses of a call already written reopens it, and so do the arrow keys.
  That is the gesture of someone coming back to fix an argument, and it produces
  no `input`.
- **The signature is a link** to the function's reference page, in the reader's
  language (the `lang` attribute, else the document's, else the browser's) and
  under the root of their choice (the `docs-base` attribute). The URL comes from
  the catalogue's `doc` field: a plugin function, which has no page in this
  repository, is shown without a link rather than with a dead one. The tooltip
  and the completion list follow the same language (`description_en`).
- New asset `jslt-signature.js` (pure logic, exercised under node): it joins
  `ASSET_FILES` and must be served with the others.

## urban-json 0.6.0 — 2026-11-11

Four categories filled (162 → 182) and one output defect fixed.

### Fixed

- **Python `repr` could leak into the JSON produced.** `to_text` returned
  `str(value)` for an array or object, hence the *Python* representation, single
  quotes included: `concat($.l, ",")` on `[[1,"x"], 2]` returned `"[1, 'x'],2"`,
  and a composite `groupby` / `countby` key gave `"[1, 'x']"`. The `#string` cast,
  by contrast, went through JSON: two text-conversion paths coexisted, one
  correct and one not. Only one remains, the compact-JSON one — which is also
  what `token.ToString()` returns on the Newtonsoft side.

### Added — 20 functions

- **Deep structures**: `flattenobject`, `unflatten` (numeric segments only become
  arrays on request: a key "2026" is a year's name in plenty of documents),
  `walk` (leaves first, so a rule depending on children works), `prune`,
  `setpath`, `unsetpath`.
- **Output**: `to_csv` (RFC 4180, columns = union of keys, nested values
  flattened into dotted keys), `to_xml` (`parsexml` conventions: `@attribute`,
  `#text`, array = repeated element), `to_yaml` (block or JSON style;
  acknowledged subset, no anchors or tags). All three are **dependency-free**.
- **Quality and diagnostics**: `require` (requires a **present** value: `0`,
  `false` and `""` are values), `requirethat` (requires a strictly true
  condition), `trace` / `traces` (observing without polluting the output; the
  journal lives on the context, so two runs never mix), and the validators
  `isemail`, `isurl`, `isuuid`, `isiban` (structure **and** modulo-97 check
  digits).
- **One reference page per function**, in both languages
  (`docs/fonctions/<name>.md` and `.en.md`, plus an index): signature, arguments
  and description, **generated** from the registry by
  `packages/urban-json/scripts/generate_function_docs.py` — a hand copy would
  have aged at the first widened signature, and a test refuses a page that no
  longer follows the registry. It is the stable URL the editor can derive from
  the function's name alone, where an anchor in a chapter breaks silently at the
  first renamed heading. The examples and the prose stay in the chapters.
- **Every description is translated** (`description_en`): the English page has no
  other source, and the intellisense now speaks the reader's language.
- **Sorting and grouping, the finishing touches**: `unzip` (the converse of
  `zip`, which had none), `sumby` and `avgby` (a per-group total took four nested
  functions for the most frequent use of grouping; the aggregated value is lazy,
  omitted it means the element, and a non-numeric value raises as for `sum`).

### Changed — widened, compatible signature

- `merge(a, b, deep, arrays)`: a 4th argument to **concatenate** arrays instead
  of replacing them. Replacement stays the default, since merging two lists of
  different lengths has no single meaning.
- `sort(l, key, descending)`: `descending` accepts an **array of booleans**, one
  direction per key (`sort($.l, [$.a, $.b], [true, false])`). The single boolean
  stays valid and unchanged. A missing direction means ascending; a direction
  **too many raises**, because that is the likeliest authoring mistake and it
  would leave a sort that looks right. That form compares component by component,
  hence slightly slower — it alone.
- `groupby(l, key, nested)`: a 3rd argument to **nest** one object level per key,
  instead of the textual key `["FR","Lyon"]` that had to be parsed back. The flat
  shape stays the default. Nesting requires the same number of keys for every
  element: otherwise one key would carry both elements *and* a subgroup, and one
  of the two would disappear — that case raises.

### Documented internals

- `FunctionInfo` carries `description_en` (the same description in English) and
  `doc` (the reference page, `"fonctions/<name>"` for the core, `None` for a
  function whose page this repository does not hold). Both are in `catalog()`:
  that is where the editor takes the tooltip and its link from. `register()` and
  `jslt_function()` accept them as trailing keyword arguments — an existing call
  is unchanged.
- `RuntimeContext` now carries `traces` (the list of observations), readable by
  an integrator after the run. An added attribute; nothing is removed.
- New internal modules: `functions/deep.py`, `functions/quality.py`,
  `functions/_writers.py` (the three emitters), `functions/bykey.py`.
- `groupby` and `countby` moved out of `functions/aggregate.py` into
  `functions/bykey.py`, along with `sumby` and `avgby`: they share a key computed
  per element, not the aggregates' convention. Nothing changes for a template
  (the registry resolves by **name**); only a direct import of the module is
  affected.

### Still not addressed

- **Dates**: `fromunix` / `tounix` (and `convert(x, "datetime")` still returns the
  epoch as **text**, which looks like a date without being one), ISO 8601
  durations, `daterange`.
- **Security**: encryption, JWT, base32, `uuid` v5/v7, masking.
- **Sorting**: no `minby` / `maxby` (the element carrying the extremum), and no
  ranking (`rank`) either.
- **Language**: functions defined inside the template, inclusion, string
  interpolation — ANTLR grammar, Java required.

## urban-json 0.5.0 — 2026-11-11

Fixes a wrong sort and fills four categories of functions (135 → 162).

### Fixed

- **Multi-key sorting was wrong on numbers.** The total order compared arrays and
  objects by their **compact JSON**, hence by code point: `sort($.l, [$.a, $.b])`
  — the natural use of a key, since it is an expression that may return an array
  — placed `[10]` before `[2]`. Arrays are now compared **element by element** (a
  prefix comes before the sequence it prefixes) and objects by their sorted keys
  then their values. Invisible while sorting scalars; silently wrong otherwise.

### Added — 27 functions

- **Collections**: `skip` (the complement of `limit`, without which there was no
  pagination), `flatten` (recursive, where `union` only descends one level),
  `zip`, `chunk`, `window`, `partition`, `distinctby`, `intersect`, `difference`.
- **Statistics**: `variance`, `stddev` (population by default), `percentile`
  (linear interpolation, so `percentile(v, 50)` agrees with `median`), `mode` (on
  any values, not only numbers), `groupby` (as an **object**, hence reducible
  with `entries`), `countby`.
- **Text**: `splitstring` (the **whole** separator: `split` only keeps its first
  character, .NET fidelity), `splitregex`, `shorten` (ellipsis, suffix included
  in the length, cuts at the last space), `slugify`, `levenshtein`, `similarity`.
- **Numbers**: `ceil` (`floor` existed alone), `log` with a free base, `tobase` /
  `frombase` (2 to 36), `isfinite`, `isnan`.

### Changed — widened, compatible signatures

- `indexof` / `lastindexof` accept an **array** (position, or `-1`). On an array
  the equality is **structural**: searching for `2` does not find `"2"`, where
  `contains` keeps the language's `==` equality out of .NET fidelity.
- `reverse` accepts a **string** (it used to return `null`) and works by
  grapheme: on a decomposed "é", reversing code points would stick the accent
  onto the neighbouring letter.
- `floor`, `ceil` and `truncate` accept a precision in decimals.

### Changed — behaviour

- `log(1000, 10)` returns exactly `3.0`: bases 10 and 2 go through their
  dedicated function, because dividing two logarithms returns
  `2.9999999999999996` — a number that would come straight out in the JSON
  produced.

### Documented internals

- `functions/folding.py` (Unicode folding) and `functions/similarity.py`
  extracted from `text.py`, `functions/_lazy.py` shared by every function with a
  computed key. These are undocumented internal modules: no guarantee, but it is
  noted here because the layout of `functions/` serves as a map.

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
