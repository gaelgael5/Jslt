# Text, regular expressions and formatting — jslt guide

*[Français](texte.md) · English*

[← jslt guide](guide.en.md) · the examples on this page are **run by the test
suite** (`tests/test_guide_examples.py`) as *template → input → output* triples.

---

## Text: `upper`, `lower`, `trim`, `split`, `startswith`, `stringcontains`…

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

---

## Regular expressions: `regexismatch`, `regexmatches`

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

---

## Unicode: `normalize`

`normalize` composes Unicode characters (form C).

---

## Formatting: `format`

`format(value, mask, culture)` follows .NET masks: numbers (`N2`, `C`, `P1`,
`D5`, `#,##0.00`…) and dates — an ISO 8601 string is a date — (`d`, `D`,
`dd/MM/yyyy`, `dddd d MMMM yyyy`…). Cultures: invariant (empty), `en-US`,
`en-GB`, `fr-FR`, `de-DE`, `es-ES`, `it-IT`. A mask outside this subset raises
an error rather than an approximate text.

The UTC offset can be written too (`zzz`, `zz`, `z`, and `K`, which yields `Z`
for UTC and nothing for a date without a timezone), so that
`parsedate(…, timezone)` and `format` round-trip. As in .NET, a **lone**
specifier (`"z"`, `"K"`) is read as a standard mask and refused: write it inside
a longer mask (`"HH:mmK"`).

```jslt
{ "prix": format($.p, "#,##0.00"), "jour": format($.d, "dddd d MMMM yyyy", "fr-FR"), "code": format($.n, "D5") }
```
```json
{ "p": 1234.5, "d": "2026-10-22T14:05:00", "n": 42 }
```
```json
{ "prix": "1,234.50", "jour": "jeudi 22 octobre 2026", "code": "00042" }
```

---

## Extracting and replacing: `substring`, `replace`, `regexreplace`

The engine could **measure** a string (`indexof`, `lastindexof`,
`stringlenght`) without being able to cut a piece out of it: bounds were computed
with nothing to consume them.

| Function | Purpose |
|---|---|
| `substring(t, start, length)` | piece of a string; negative `start` = from the end, missing `length` = to the end |
| `replace(t, search, replacement)` | every occurrence, plain text |
| `regexreplace(t, pattern, replacement)` | by regular expression, with `$1`, `${name}`, `$&` |
| `trimstart(t, chars)` / `trimend(t, chars)` | directed trimming |
| `repeat(t, n)` | repetition (`n` ≤ 0: empty string) |
| `titlecase(t)` | initial capital on each word, **the rest untouched** |

**Tolerant bounds.** .NET's `Substring` throws as soon as the bounds leave the
string; here an out-of-range start yields an empty string and an over-long length
stops at the end. A template transforms data it does not choose: hitting a field
shorter than expected must not fail the whole transformation. A **negative**
length does raise: that is an authoring mistake, not surprising data.

**`titlecase` lowers nothing.** A plain `str.title()` would turn a correct
"McDonald" into "Mcdonald". On names coming from real data that is a
degradation: only the first letter of each word is touched.

```jslt
{
  "code": substring($.address, -5, 5),
  "street": substring($.address, 0, 16),
  "digits": replace($.phone, "-", ""),
  "name": titlecase($.name)
}
```

```json
{ "address": "12 rue des Lilas 75011", "phone": "01-02-03-04-05", "name": "ana McDonald" }
```

```json
{
  "code": "75011",
  "street": "12 rue des Lilas",
  "digits": "0102030405",
  "name": "Ana McDonald"
}
```

**`regexreplace` follows the .NET syntax** for replacements: `$1` for a numbered
group, `${name}` for a named group, `$&` for the whole match, `$$` for a literal
`$`. It is translated into the Python dialect, so a replacement written for .NET
behaves the same.

Mind the convention: like `regexismatch` and `regexmatches`, `regexreplace`
**converts a scalar to text** (`42` becomes `"42"`), where `replace` would return
`false`. Searching for a pattern in a number makes sense; upper-casing it does
not.

```jslt
{ "iso": regexreplace($.d, "(\\d{2})/(\\d{2})/(\\d{4})", "$3-$2-$1") }
```

```json
{ "d": "24/12/2026" }
```

```json
{ "iso": "2026-12-24" }
```

## Comparing without case or accents: `foldtext`, `deaccent`

`normalize` now accepts a **form** (`C` by default, `D`, `KC`, `KD`).
`deaccent` strips diacritics without touching case. `foldtext` returns a
**comparison key**: lowercase *and* unaccented by default, or only `case`, or
only `accents`.

Why a key rather than a "case-insensitive" operator? Because a second `==` would
have doubled the semantics of the first, and because the same key also serves to
**sort** (see [`sort`](collections.en.md#sorting-and-ordering-sort-reverse-first-last)).

```jslt
{
  "same": foldtext($.a) == foldtext($.b),
  "unaccented": deaccent($.a),
  "key": foldtext($.a)
}
```

```json
{ "a": "CRÈME", "b": "creme" }
```

```json
{ "same": true, "unaccented": "CREME", "key": "creme" }
```

---

**See also**: [Dates and times](dates.en.md) to read a date (`parsedate`) and compute with it.

---

[← jslt guide](guide.en.md)
