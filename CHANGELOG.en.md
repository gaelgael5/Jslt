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

## urban-json 0.8.0 — 2026-11-11

The language's elementary gaps, filled (182 → 210): walking an array with an
expression, creating one, splitting a text, **choosing** a value from a
condition, reading a **computed** key, and rounding like an invoice.

### Added — walking with an expression

`map`, `filter`, `find`, `findindex`, `every`, `some`, `reduce`, `minby`,
`maxby`, `cumsum`. The `{"$source": …}` loop already did the job of `map`, but
**in value position only**: it could not be passed as an argument to a function.
`reduce` had no equivalent at all — yet it is the general fold of which `sum`,
`product` and `sumby` are special cases.

- `reduce` presents `{acc, value, index}` as the **current source**: a jslt
  expression has only one source, and the language has no second parameter. With
  no initial value, the fold starts from the first element.
- `some` and `every` rather than `any` and `all`: `any` already exists with the
  .NET meaning "non-empty array", and giving it a predicate would have silently
  changed the result of ported templates.
- `every` of an empty array is **true** (no counter-example), `some` is false.
- `minby` / `maxby` return the **element**, where `min` / `max` return the
  extreme value without saying who carries it.

### Added — building and editing an array

`range`, `slice`, `append`, `insert`, `removeat`. `range` is the **only**
function in the engine that creates a series: everything else transforms what
comes in, and "the twelve months" was inexpressible unless the data carried
them. End **excluded** and a single argument counting from zero, to line up with
the indices of `skip` and `slice`; a zero step and series of more than a million
elements are **refused**, because this is the only place where a template can
ask for an outsized array. The four edits return a **copy**.

### Added — splitting a text

`chars` (by grapheme), `lines` (all three line endings, empty ones included),
`words`, `removeprefix` / `removesuffix`, `capitalize`. Three of these needs had
an answer that **looked** like it worked: `splitstring($.t, "")` returns the
whole text, `trimstart` removes a **set of characters** and not a prefix (on
"bacab", `trimstart($.t, "ab")` returns "cab" although the prefix is not there),
and `titlecase` upper-cases **every** initial.

### Added — a conditional in expression position

`ifelse(condition, if_true, if_false)`. The language had **none**: `when`
switches on a **value** (it compares `==` against each case name), so a composed
condition — `$.n > 10 && $.actif` — first had to be computed, then switched on
its `"true"` / `"false"` text. It was the engine's most elementary gap, and the
only one with no readable workaround.

Only the **chosen** branch is evaluated (lazy arguments), so
`ifelse($.d == 0, 0, 100 / $.d)` is safe: with evaluated arguments, the function
would have been useless exactly where it is most wanted. The condition reads like
`filter`'s, not like `requirethat`'s assertion. Real `if … else` syntax would
require changing the ANTLR grammar, hence `java`, absent from the container — the
function gets the same semantics without touching it.

### Added — access by computed key

`get(value, key)` and `getpath(value, path, separator)`. A path is **literal**:
`$.o[$.k]` is not a supported selector, and `select` too only accepts a path
written in the template. Reading a configuration whose keys *are* data required a
detour through `entries` + `filter` + a variable — four functions for one key
lookup.

- Missing key, out-of-bounds index, source that is neither object nor array:
  `null`, the objects family's convention. No fallback argument: `??` already
  says it, and a fallback as an argument would be evaluated even when the key
  exists; to require the value, `require(get(…), "message")`.
- `get` accepts a **negative** index (from the end), like `slice`.
- `getpath` is the reciprocal of `setpath`, which had none: same steps, array
  indices included, same adjustable separator.

### Added — the roundings `round` cannot do

`roundhalfup`, `roundto`, `toprecision`. `round` is **banker's** rounding (a kept
quirk): `round(0.125, 2)` gives `0.12` where an invoice expects `0.13`. The
engine therefore could not write the commonest rounding in commerce, nor round to
a multiple (a till's 0.05 step), nor to a number of **significant** digits.

- Halves go **away from zero**: `-0.5` gives `-1`, so that a credit note rounds
  like the invoice it cancels.
- All three read the number as it is **written**: `2.675` is stored as
  `2.67499999…`, and that is what the workaround `round($.n * 20) / 20`
  returned.
- A zero or negative step **raises**, rather than returning a value that was
  rounded to nothing.

### Changed — widened, compatible signature

- `indexof(text_or_array, value, start)`: a 3rd argument, the starting position.
  Walking every occurrence used to mean re-splitting the text at each turn.
- `stringlength` **spells** `stringlenght` correctly, the original name being a
  typo. Both names register the **same** implementation, so they cannot diverge;
  removing the old one would break the templates written with it.
- Seven registry descriptions clear up a neighbouring name right where the reader
  meets it — in the editor's tooltip: `join` points to `concat` (joining text),
  `any` to `some`, `split` to `splitstring`, `round` to `roundhalfup`, `index` to
  `get`. The guide carries the full table ("Misleading names").

### Documented internals

- New modules: `functions/iteration.py`, `functions/sequences.py`,
  `functions/textparts.py`, `functions/conditions.py`, `functions/access.py`,
  `functions/rounding.py`.

## urban-json 0.7.0 — 2026-11-11

Three operators returned a **wrong answer** where they could not give a right
one. An answer goes unnoticed; an error does not.

### Fixed

- **`==` on two containers always said `false`.** Two identical objects, two
  identical arrays: `false`, and `!=` said `true`. There was no structural
  equality in the language at all, and nothing signalled it. Equality now
  descends into arrays (same length, element by element) and objects (same keys,
  same values), **with the language's rule** — `[2] == ["2"]` is true, just as
  `2 == "2"` is at the first level. To tell a number from its text, use
  `indexof([$.a], $.b) == 0`.
- **`+` on two arrays said `false`.** It **concatenates**, as for two strings.
  Between two objects it **raises**, naming `merge`, which carries the options
  (deep, arrays) a silent `+` would hide; between an array and a value it raises
  naming `union`, because "append an element" and "concatenate" are equally
  defensible readings.
- **`"text" + $.array` leaked the Python `repr`** (`a[1, 'x']`). That is the
  defect fixed in 0.6.0 inside `to_text`… which the operators' private copy had
  kept. Both copies are replaced by a leaf module, `urban_json._text`: there is
  now **one** text rendering in the engine, and it is compact JSON.
- **`- * / % & | ^` and `< <= > >=` on a container** returned `false`. They
  raise. For comparisons `false` was contradictory too: `a < b` and `a >= b`
  cannot both be false. Ordering between containers exists, but it is `sort`'s,
  not the operators'.

`null` is not a container: it keeps its historical fallback to `false`
(`$.absent + 1` returns `false`), which templates rely on.

### Why a minor and not a patch

An existing template can change output: a comparison that was `false` may become
`true`, and an operation that returned `false` may now raise. That is the point
of the fix, but it is visible from the outside.

## Plugins — 2026-11-11

Versions ready to be published alongside the 0.6.0 core.

- **urban-json-csv 0.2.0** and **urban-json-xml 0.2.0**: `parsecsv` and
  `parsexml` (reading from a **string**, with no file), which came with the 0.4.0
  core and have never been published since. Both READMEs are also cleaned of
  their pointers to the .NET engine.
- **urban-json-db 0.1.2**, **urban-json-html 0.1.2**, **urban-json-random
  0.1.2**: documentation only. The passages that explained a behaviour by
  comparison with .NET now state the behaviour; in `random`, "Deliberate
  deviations from .NET" becomes "Drawing rules". A PyPI version being immutable,
  a corrected description only reaches the index through a patch.
- Unchanged, hence not republished: `urban-json-files`, `urban-json-excel`,
  `urban-json-phone`, `urban-json-elastic`, `urban-json-http`.

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
  first renamed heading. **Every page carries an executed example**: the
  signature alone says neither what goes in nor what comes out. The 185 examples
  are replayed by the guide suite, hence by both engines; the chapters keep the
  prose and the *usage* examples, which mix several functions. The pages also
  carry a **comment per example**, a **"Good to know"** section (69 functions:
  refusals, defaults, traps) and the **role of each argument** where it cannot be
  guessed (13 functions). `parsedate` is the showcase: seven commented cases,
  including reading an **English** date, and the rule that was missing — with no
  mask, only numeric forms and ISO are recognised, so "November 11, 2026" raises
  even in `en-US`. The [Dates and times](docs/dates.en.md) chapter gains the
  matching section.
- **The guide no longer explains itself through .NET.** ".NET mask", "as in
  .NET", ".NET quirk preserved": some thirty pointers replaced the explanation
  with a reference to an engine the reader of the Python library does not have
  and cannot consult. Each one is replaced by **what it pointed at** — first of
  all the complete mask vocabulary of `format` (numbers: `N`, `F`, `C`, `P`,
  `D`, `X`, `E`, `G` and the custom masks `0 # . , %`; dates: the one-letter
  standards, the tokens being shared with `parsedate`; the seven cultures and
  what they fix), which until now fitted in "follows .NET masks". A test now
  refuses any mention inside `docs/`. The porting provenance stays in
  `CLAUDE.md` and in this changelog, and the packages' READMEs keep their
  attribution line: citing the origin is not explaining through it.
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
