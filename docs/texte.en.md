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

**See also**: [Dates and times](dates.en.md) to read a date (`parsedate`) and compute with it.

---

[← jslt guide](guide.en.md)
