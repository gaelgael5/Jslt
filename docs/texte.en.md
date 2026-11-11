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

## Splitting precisely: `splitstring`, `splitregex`

**`split` only keeps the first character of the separator.** That is .NET
fidelity, and it is a trap: `split($.t, ", ")` cuts on the comma and leaves the
spaces, silently. Hence two functions rather than a change to `split`, which
would break ported templates:

- `splitstring(t, separator, limit)` cuts on the **whole** separator, at most
  `limit` times;
- `splitregex(t, pattern, limit)` cuts on a pattern, for separators of varying
  shape (`"a ; b;c"`).

```jslt
{
  "trap": split($.t, ", "),
  "correct": splitstring($.t, ", "),
  "varying": splitregex($.v, "\\s*;\\s*")
}
```

```json
{ "t": "a, b, c", "v": "a ; b;c" }
```

```json
{ "trap": ["a", " b", " c"], "correct": ["a", "b", "c"], "varying": ["a", "b", "c"] }
```

## Shortening, reversing, identifying

| Function | Purpose |
|---|---|
| `shorten(t, length, suffix)` | shortens with an ellipsis, **suffix included** in the length |
| `reverse(t)` | reverses a text (or an array) |
| `slugify(t, separator)` | URL identifier: unaccented, lowercase, words joined |

The name is not `truncate`: that one is already taken by **numeric** truncation.
The suffix counts towards the requested length, otherwise "at most 8 characters"
would return 9 and overflow the column you were trying to fit. And when the cut
falls in the middle of a word, `shorten` backs up to the last space — "Paris L…"
makes the reader see a word that does not exist; with no space in the window (an
identifier, a very long word) it cuts hard rather than losing everything.

`reverse` now accepts a string (it used to return `null`), and reverses by
**grapheme**: on an "é" written in decomposed form, reversing code points would
stick the accent onto the neighbouring letter.

```jslt
{
  "short": shorten($.t, 12),
  "slug": slugify($.t),
  "backwards": reverse($.word)
}
```

```json
{ "t": "Crème Brûlée à Paris", "word": "été" }
```

```json
{ "short": "Crème…", "slug": "creme-brulee-a-paris", "backwards": "été" }
```

## Matching two spellings: `levenshtein`, `similarity`

`==` answers "identical or not", `foldtext` reconciles case and accents; what
remains is the typo. `levenshtein(a, b)` counts the characters to insert, delete
or replace; `similarity(a, b)` scales that count between 0 and 1, which is easier
to threshold. Two empty strings score 1: they are identical, and returning
"undefined" would force every caller to handle that case.

The cost is O(n·m): this is the tool for labels, not for documents.

```jslt
{
  "distance": levenshtein($.a, $.b),
  "close": similarity(foldtext($.a), foldtext($.b)) > 0.8
}
```

```json
{ "a": "Crème brulee", "b": "creme brûlée" }
```

```json
{ "distance": 4, "close": true }
```

---

**See also**: [Dates and times](dates.en.md) to read a date (`parsedate`) and compute with it.

---

[← jslt guide](guide.en.md)
