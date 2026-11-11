<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# Function reference

*[Français](sommaire.md) · English*

One page per function, generated from the registry: signature, arguments and description. The prose and the examples live in the guide's chapters.

## [Data and collections](../collections.en.md)

| Function | Description |
|---|---|
| [`any`](any.en.md) | True when the source is a non-empty array |
| [`avg`](avg.en.md) | Mean of the numbers in an array (null for an empty array) |
| [`avgby`](avgby.en.md) | Mean per computed key, as an object { key: mean } (the value defaults to the element) |
| [`chunk`](chunk.en.md) | Cuts an array into consecutive slices of size elements |
| [`concat`](concat.en.md) | Joins the elements of an array into text, separated by split_char then delimit_char |
| [`contains`](contains.en.md) | True when the array holds an element equal to the value |
| [`convert`](convert.en.md) | Converts a value to a type: integer, decimal, string, boolean (uri, uuid, datetime, time as text) |
| [`count`](count.en.md) | Number of items: elements of an array, keys of an object, characters of a text, 0 for null |
| [`countby`](countby.en.md) | Counts the elements of an array per computed key, as an object { key: count } |
| [`createindex`](createindex.en.md) | Builds an index {key: element} from a source, a splitting path and a key path |
| [`difference`](difference.en.md) | Elements of the left array absent from the right one, deduplicated |
| [`distinct`](distinct.en.md) | Unique values selected by a JSONPath path in an array, in order of appearance |
| [`distinctby`](distinctby.en.md) | Deduplicates an array on a key computed per element, keeping the first |
| [`first`](first.en.md) | First element of an array, or null when it is empty |
| [`flatten`](flatten.en.md) | Flattens an array of arrays, all the way down by default or over depth levels |
| [`group`](group.en.md) | Groups an array by successive JSONPath paths into nested {Label, Items} |
| [`groupby`](groupby.en.md) | Groups an array into an object { key: elements }, key computed per element; nested adds one level per key of an array of keys |
| [`index`](index.en.md) | Element of an index (built by createindex) for a key, or null |
| [`intersect`](intersect.en.md) | Elements of the left array also present on the right, deduplicated |
| [`join`](join.en.md) | Left join: attaches to the left objects the right elements sharing the key |
| [`last`](last.en.md) | Last element of an array, or null when it is empty |
| [`limit`](limit.en.md) | The first max_items elements of an array |
| [`median`](median.en.md) | Median value of the numbers in an array (null for an empty array) |
| [`mode`](mode.en.md) | Most frequent value of an array (the first one seen in case of a tie) |
| [`partition`](partition.en.md) | Splits an array into { true, false } according to a predicate evaluated per element |
| [`percentile`](percentile.en.md) | Percentile p (0 to 100) of the numbers in an array, by linear interpolation |
| [`product`](product.en.md) | Product of the numbers in an array (1 for an empty array) |
| [`reverse`](reverse.en.md) | Reverses the order of an array or of a text, without modifying the source |
| [`select`](select.en.md) | First value selected by a JSONPath path in the source, or null |
| [`selectany`](selectany.en.md) | True when the JSONPath path selects at least one value in the source |
| [`selectmany`](selectmany.en.md) | All the values selected by a JSONPath path in the source |
| [`skip`](skip.en.md) | Drops the first n elements of an array (the complement of limit) |
| [`sort`](sort.en.md) | Sorts an array: on the elements, or on a key computed per element, smallest first (descending true, or one direction per key, for the reverse) |
| [`stddev`](stddev.en.md) | Standard deviation of the numbers in an array: of population by default, of sample when sample is true |
| [`sum`](sum.en.md) | Sum of the numbers in an array (0 for an empty array or null) |
| [`sumby`](sumby.en.md) | Sum per computed key, as an object { key: sum } (the value defaults to the element) |
| [`union`](union.en.md) | Flattens an array of arrays by one level |
| [`unzip`](unzip.en.md) | Converse of zip: from an array of rows, returns one array per position |
| [`variance`](variance.en.md) | Variance of the numbers in an array: of population by default, of sample when sample is true |
| [`window`](window.en.md) | Sliding windows of size consecutive elements (empty when the array is shorter) |
| [`zip`](zip.en.md) | Pairs two arrays element by element, stopping at the shorter one |

## [Dates and times](../dates.en.md)

| Function | Description |
|---|---|
| [`dateadd`](dateadd.en.md) | Adds a duration to an ISO 8601 date: unit second, minute, hour, day, week, month or year, and a whole number (negative to subtract) |
| [`datediff`](datediff.en.md) | Counts the whole units elapsed between two ISO 8601 dates: second, minute, hour, day, week, month or year, negative when the end precedes the start |
| [`dateduration`](dateduration.en.md) | Splits the interval between two dates into years, months, days, hours, minutes and seconds |
| [`dateendof`](dateendof.en.md) | Last instant of the period holding the date (inclusive bound, to the microsecond) |
| [`datepart`](datepart.en.md) | Extracts a whole component from an ISO 8601 date: year, month, day, dayofweek (Sunday = 0), hour, minute or second |
| [`datestartof`](datestartof.en.md) | First instant of the period holding the date: year, quarter, month, week (Monday), day, hour or minute |
| [`datesub`](datesub.en.md) | Subtracts a duration from an ISO 8601 date: unit second, minute, hour, day, week, month or year, and a whole number |
| [`datezone`](datezone.en.md) | Attaches a timezone to a date without offset, or converts a date that already carries one |
| [`now`](now.en.md) | Current date and time in ISO 8601: local, or UTC when utc is true |
| [`parsedate`](parsedate.en.md) | Reads a date from text and returns it in ISO 8601: detection by culture, or an explicit mask (dd/MM/yyyy…), with an optional timezone |
| [`today`](today.en.md) | Today's date at midnight in ISO 8601: local, or UTC when utc is true |

## [Encoding, digests and escaping](../encodage.en.md)

| Function | Description |
|---|---|
| [`crc32`](crc32.en.md) | CRC32 checksum of a value (unsigned integer) |
| [`frombase64`](frombase64.en.md) | Decodes Base64 text into UTF-8 text |
| [`hexdecode`](hexdecode.en.md) | Reads hexadecimal text back into a UTF-8 string |
| [`hexencode`](hexencode.en.md) | Writes the UTF-8 bytes of a value in hexadecimal |
| [`hmacsha256`](hmacsha256.en.md) | HMAC-SHA256 signature of a value with a secret key, in hexadecimal |
| [`htmlescape`](htmlescape.en.md) | Escapes the characters that mean something in HTML (< > & " ') |
| [`htmlunescape`](htmlunescape.en.md) | Replaces HTML entities (&amp;, &lt;…) with their characters |
| [`md5`](md5.en.md) | MD5 digest of a value, in hexadecimal (identity, not signature) |
| [`sha1`](sha1.en.md) | SHA-1 digest of a value, in hexadecimal (identity, not signature) |
| [`sha256`](sha256.en.md) | SHA-256 digest of a value, in hexadecimal |
| [`sha512`](sha512.en.md) | SHA-512 digest of a value, in hexadecimal |
| [`tobase64`](tobase64.en.md) | Encodes a value in Base64 (UTF-8 text; object or array serialised as JSON) |
| [`urldecode`](urldecode.en.md) | Decodes a value coming from a URL (%20, %C3%A9…) |
| [`urlencode`](urlencode.en.md) | Encodes a value for a URL (path mode to keep the slashes) |

## [Expressions and operators](../expressions.en.md)

| Function | Description |
|---|---|
| [`param`](param.en.md) | Value of an external parameter passed to transform, or the fallback value |
| [`params`](params.en.md) | All the external parameters of the run, as an object |
| [`uuid`](uuid.en.md) | A new random unique identifier (UUID v4) on each call |

## [Numbers and maths](../nombres.en.md)

| Function | Description |
|---|---|
| [`abs`](abs.en.md) | Absolute value of a number (null when it is not a number) |
| [`acos`](acos.en.md) | Arc cosine, in radians |
| [`acosh`](acosh.en.md) | Hyperbolic arc cosine |
| [`asin`](asin.en.md) | Arc sine, in radians |
| [`asinh`](asinh.en.md) | Hyperbolic arc sine |
| [`atan`](atan.en.md) | Arc tangent, in radians |
| [`atan2`](atan2.en.md) | Angle in radians of the point (x = right, y = left): atan2(y, x) |
| [`atanh`](atanh.en.md) | Hyperbolic arc tangent |
| [`ceil`](ceil.en.md) | Rounds up, to the integer (2.1 -> 3.0) or to digits decimals |
| [`clamp`](clamp.en.md) | Brings a number back into the [lower, upper] range |
| [`cos`](cos.en.md) | Cosine of an angle in radians |
| [`cosh`](cosh.en.md) | Hyperbolic cosine |
| [`e`](e.en.md) | The constant e, base of the natural logarithm (2.71828…) |
| [`exp`](exp.en.md) | Exponential: e raised to the power of the number |
| [`floor`](floor.en.md) | Rounds down, to the integer (2.7 -> 2.0) or to digits decimals |
| [`frombase`](frombase.en.md) | Reads an integer written in a base from 2 to 36 |
| [`fromhex`](fromhex.en.md) | Reads an integer written in hexadecimal (with or without the 0x prefix) |
| [`gcd`](gcd.en.md) | Greatest common divisor of two integers |
| [`isfinite`](isfinite.en.md) | True when the value is a finite number (neither infinite nor NaN) |
| [`isnan`](isnan.en.md) | True when the value is the undefined result of a computation (NaN) |
| [`log`](log.en.md) | Logarithm of a number in the given base |
| [`logarithm`](logarithm.en.md) | Natural logarithm (base e) of a number |
| [`logarithm10`](logarithm10.en.md) | Common logarithm (base 10) of a number |
| [`logarithm2`](logarithm2.en.md) | Binary logarithm (base 2) of a number |
| [`max`](max.en.md) | Larger of two numbers, or of the given array (decimal for two numbers) |
| [`min`](min.en.md) | Smaller of two numbers, or of the given array (decimal for two numbers) |
| [`parsenumber`](parsenumber.en.md) | Reads a number written as text according to a culture (1 234,56 in fr-FR) |
| [`pi`](pi.en.md) | The constant pi (3.14159…) |
| [`pow`](pow.en.md) | Power: base raised to the exponent, returned as a decimal |
| [`round`](round.en.md) | Rounds to the nearest integer, halves to even (2.5 -> 2.0, 3.5 -> 4.0), returned as a decimal |
| [`shiftleft`](shiftleft.en.md) | Shifts the bits of an integer to the left (multiplies by 2^bits) |
| [`shiftright`](shiftright.en.md) | Shifts the bits of an integer to the right (divides by 2^bits) |
| [`sign`](sign.en.md) | Sign of a number: -1, 0 or 1 |
| [`sin`](sin.en.md) | Sine of an angle in radians |
| [`sinh`](sinh.en.md) | Hyperbolic sine |
| [`sqrt`](sqrt.en.md) | Square root of a number |
| [`tan`](tan.en.md) | Tangent of an angle in radians |
| [`tanh`](tanh.en.md) | Hyperbolic tangent |
| [`tobase`](tobase.en.md) | Writes an integer in a base from 2 to 36, padded to width digits |
| [`tohex`](tohex.en.md) | Writes an integer in lower-case hexadecimal, padded to width digits |
| [`truncate`](truncate.en.md) | Cuts towards zero (-2.7 -> -2.0), to the integer or to digits decimals |

## [Objects and deep structures](../objets.en.md)

| Function | Description |
|---|---|
| [`entries`](entries.en.md) | Pairs of an object as an array of { key, value }, in document order |
| [`flattenobject`](flattenobject.en.md) | Flattens an object into dotted keys (a.b.c), arrays indexed by their position |
| [`fromentries`](fromentries.en.md) | Rebuilds an object from an array of { key, value } or of [key, value] pairs |
| [`has`](has.en.md) | True when the object carries that key, even with a null value |
| [`keys`](keys.en.md) | Keys of an object, in document order (null when it is not an object) |
| [`merge`](merge.en.md) | Merges two objects, the right one winning the shared keys (deep for sub-objects, arrays to concatenate arrays) |
| [`omit`](omit.en.md) | Object without the requested keys (one key or an array of keys) |
| [`pick`](pick.en.md) | Sub-object limited to the requested keys (one key or an array of keys) |
| [`prune`](prune.en.md) | Recursively removes the nulls of a structure, and the empties with the empty option |
| [`renamekeys`](renamekeys.en.md) | Renames the keys of an object according to a { old: new } mapping |
| [`setpath`](setpath.en.md) | Copy of the object with a value placed at the end of a dotted path (levels created as needed) |
| [`unflatten`](unflatten.en.md) | Rebuilds a nested object from dotted keys (arrays true for the indices) |
| [`unsetpath`](unsetpath.en.md) | Copy of the object without the dotted path (no error when it is absent) |
| [`values`](values.en.md) | Values of an object, in document order (null when it is not an object) |
| [`walk`](walk.en.md) | Applies an expression to every node of a structure, from the leaves to the root |

## [Quality: refuse, observe, validate](../qualite.en.md)

| Function | Description |
|---|---|
| [`isemail`](isemail.en.md) | True when the text has the shape of an email address |
| [`isiban`](isiban.en.md) | True when the text is an IBAN whose check digits (modulo 97) are right |
| [`isurl`](isurl.en.md) | True when the text has the shape of a URL with its scheme |
| [`isuuid`](isuuid.en.md) | True when the text has the shape of a UUID (braces tolerated) |
| [`require`](require.en.md) | Returns the value when it is present, otherwise raises with the given message |
| [`requirethat`](requirethat.en.md) | Checks a condition and raises with the given message when it is not true |
| [`trace`](trace.en.md) | Returns the value unchanged and records it in the journal, readable through traces() |
| [`traces`](traces.en.md) | Journal of the values observed by trace() in this run |

## [Text output](../sortie.en.md)

| Function | Description |
|---|---|
| [`to_block`](to_block.en.md) | Output: one compact JSON line per element of the resulting array (JSON Lines), or the resulting object on one line |
| [`to_csv`](to_csv.en.md) | Output: the resulting array as CSV (separator and header row adjustable) |
| [`to_json`](to_json.en.md) | Output: serialises the result as JSON, indented when indented is true; ignore_null_and_empty_value drops the null or empty properties |
| [`to_xml`](to_xml.en.md) | Output: the result as XML under the given root element (@key = attribute, #text = content) |
| [`to_yaml`](to_yaml.en.md) | Output: the result as YAML, in block style or in JSON style when json_style is true |

## [Text, regular expressions and formatting](../texte.en.md)

| Function | Description |
|---|---|
| [`deaccent`](deaccent.en.md) | Removes diacritics (accents, cedillas) without touching the case |
| [`endswith`](endswith.en.md) | True when the text ends with txt |
| [`foldtext`](foldtext.en.md) | Comparison key for a text: lowercase without accents by default, or case / accents only |
| [`format`](format.en.md) | Formats a number or a date (ISO string) with a .NET mask and a culture |
| [`indexof`](indexof.en.md) | Position (from 0) of the first occurrence in a text or an array, -1 when absent |
| [`lastindexof`](lastindexof.en.md) | Position (from 0) of the last occurrence in a text or an array, -1 when absent |
| [`levenshtein`](levenshtein.en.md) | Number of characters to insert, delete or replace to go from one text to the other |
| [`lower`](lower.en.md) | Text in lower case (null stays null, a non-string gives false) |
| [`normalize`](normalize.en.md) | Normalizes a Unicode string: form C (default), D, KC or KD |
| [`padleft`](padleft.en.md) | Pads the text on the left up to length with the 1st character of charset (space by default) |
| [`padright`](padright.en.md) | Pads the text on the right up to length with the 1st character of charset (space by default) |
| [`regexismatch`](regexismatch.en.md) | True when the text holds a match of the regex pattern |
| [`regexmatches`](regexmatches.en.md) | List of the matches of the regex pattern in the text |
| [`regexreplace`](regexreplace.en.md) | Replaces the matches of a regex pattern ($1, ${name}, $& for the groups) |
| [`repeat`](repeat.en.md) | Repeats the text count times (0 or negative: empty string) |
| [`replace`](replace.en.md) | Replaces every occurrence of search with replacement |
| [`shorten`](shorten.en.md) | Shortens a text to length characters at most, suffix included (… by default) |
| [`similarity`](similarity.en.md) | Closeness of two texts between 0 (all differs) and 1 (identical) |
| [`slugify`](slugify.en.md) | Turns a text into a URL identifier: no accents, lower case, words joined by a dash |
| [`split`](split.en.md) | Cuts a text into an array on the first character of charset |
| [`splitregex`](splitregex.en.md) | Cuts a text on the matches of a regex pattern |
| [`splitstring`](splitstring.en.md) | Cuts a text on a whole separator (several characters), at most limit times |
| [`startswith`](startswith.en.md) | True when the text starts with txt |
| [`stringcontains`](stringcontains.en.md) | True when the text holds contain_str |
| [`stringlenght`](stringlenght.en.md) | Number of characters of a text (0 for null or a non-string) — original spelling kept |
| [`substring`](substring.en.md) | Extracts length characters from start (negative start = from the end, length absent = to the end) |
| [`titlecase`](titlecase.en.md) | Upper-cases the first letter of every word, leaving the rest alone |
| [`trim`](trim.en.md) | Removes the spaces at both ends, or the characters of txt when it is given |
| [`trimend`](trimend.en.md) | Removes the trailing spaces, or the characters of txt |
| [`trimstart`](trimstart.en.md) | Removes the leading spaces, or the characters of txt |
| [`upper`](upper.en.md) | Text in upper case (null stays null, a non-string gives false) |

## [Types, error fallback and validation](../types.en.md)

| Function | Description |
|---|---|
| [`isarray`](isarray.en.md) | True when the value is a JSON array |
| [`isboolean`](isboolean.en.md) | True when the value is a boolean (true or false) |
| [`isnotnull`](isnotnull.en.md) | True when the value is neither null nor absent |
| [`isnull`](isnull.en.md) | True when the value is null or absent |
| [`isnumber`](isnumber.en.md) | True when the value is a number (a boolean is not one) |
| [`isobject`](isobject.en.md) | True when the value is a JSON object |
| [`isstring`](isstring.en.md) | True when the value is a string |
| [`parsejson`](parsejson.en.md) | Reads JSON text and returns the matching value (object, array or scalar) |
| [`schema`](schema.en.md) | JSON Schema (draft-04) inferred from a sample JSON fragment |
| [`schemaerrors`](schemaerrors.en.md) | List of the validation errors of a document against a JSON Schema (empty when it conforms) |
| [`schemaisvalid`](schemaisvalid.en.md) | True when the document satisfies the given JSON Schema (supported subset) |
| [`trydefault`](trydefault.en.md) | Value of the expression, or that of the fallback when the expression raises an error |
| [`typeof`](typeof.en.md) | JSON type of a value: null, boolean, number, string, array or object |

---

[← jslt guide](../guide.en.md)
