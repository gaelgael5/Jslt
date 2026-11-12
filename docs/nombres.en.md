# Numbers and math — jslt guide

*[Français](nombres.md) · English*

[← jslt guide](guide.en.md) · the examples on this page are **run by the test
suite** (`tests/test_guide_examples.py`) as *template → input → output* triples.

---

Three conventions to know before reading on: `floor`/`round`/`min`/`max` return a
**float**, `round` does **banker's rounding** (0.5 → 0, 1.5 → 2), and `min`/`max`
keep their **binary** form (two arguments) on top of accepting an array.

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

---

## Reading a number written as text: `parsenumber`

The counterpart of `parsedate`: the engine could **write** a number for a culture
(`format($.v, "N2", "fr-FR")`) without being able to read it back. A feed whose
amounts arrive as localised text was therefore not tractable.

`parsenumber(text, culture)` uses the **same** culture data as `format`, so the
round trip is closed by construction. Symbols around the number (`€`, `%`,
non-breaking thousands separators) are ignored; an integer stays an integer.
Unreadable text **raises**: returning `null` would turn a corrupted amount into
"no amount", and the total computed afterwards would be wrong with nothing to
signal it.

```jslt
{
  "fr": parsenumber($.a, "fr-FR"),
  "de": parsenumber($.b, "de-DE"),
  "us": parsenumber($.c, "en-US"),
  "back": parsenumber(format($.d, "N2", "fr-FR"), "fr-FR")
}
```

```json
{ "a": "1 234,56 €", "b": "1.234,56", "c": "1,234.56", "d": 1234.5 }
```

```json
{ "fr": 1234.56, "de": 1234.56, "us": 1234.56, "back": 1234.5 }
```

## Precision, bounds and bits

| Function | Purpose |
|---|---|
| `round(v, digits)` | **banker's** rounding, to the integer without the 2nd argument |
| `sign(v)` | `-1`, `0` or `1` |
| `clamp(v, low, high)` | brings into range; inverted bounds = error |
| `gcd(a, b)` | greatest common divisor |
| `shiftleft(v, bits)` / `shiftright(v, bits)` | bit shifts |
| `tohex(v, width)` / `fromhex(t)` | hexadecimal (`0x` accepted on reading) |

`round` kept its banker's rounding to the integer, which forced you to multiply
by 100, round and divide back — with the representation error that drags along.
The second argument does the work, **keeping banker's rounding**: `round(0.25, 1)`
gives `0.2`, not `0.3`.

Bit shifts are **functions**, not operators: adding `<<` and `>>` to the grammar
would require regenerating the ANTLR parser, whereas `&`, `|` and `^` already
exist as operators. `gcd` and the shifts require **integers** and raise on a
decimal, rather than silently truncating.

`tohex` writes the sign before the digits (`-ff`): a JSON integer has no width,
hence no natural two's-complement signed representation.

```jslt
{
  "rounded": round($.v, 2),
  "bounded": clamp($.v, 0, 10),
  "sign": sign($.v),
  "hex": tohex($.n, 4),
  "read": fromhex($.h)
}
```

```json
{ "v": 12.345, "n": 255, "h": "0x1F" }
```

```json
{ "rounded": 12.35, "bounded": 10, "sign": 1, "hex": "00ff", "read": 31 }
```

---

## Directed rounding and precision

`floor` existed **without** `ceil`: the most visible asymmetry of the port, which
forced you to write `0 - floor(0 - x)`. `ceil` is here now, and all three
directed roundings accept a precision.

| Call | Result |
|---|---|
| `ceil(2.1)` | `3.0` |
| `ceil(1.2345, 2)` | `1.24` |
| `floor(1.2345, 2)` | `1.23` |
| `truncate(-1.2345, 2)` | `-1.23` (towards zero) |
| `floor(-1.2345, 2)` | `-1.24` (downwards) |

`truncate` cuts towards zero, `floor` goes down: on a negative number the two
differ, which is the whole point of having both. `round` remains **banker's**
rounding (see above).

### Commercial rounding, to a multiple, to significant digits

`round` is the **banker's** rounding: halves go to the even digit, so
`round(0.125, 2)` gives `0.12` where an invoice expects `0.13`. Three functions
cover what that choice leaves out.

| Function | Role |
|---|---|
| `roundhalfup(v, decimals)` | commercial rounding: halves go **away from zero** (`-0.5` → `-1`) |
| `roundto(v, step)` | rounds to the nearest multiple: a till's 0.05 step, the quarter hour |
| `toprecision(v, digits)` | rounds to a number of **significant** digits, not decimals |

All three read the number as it is **written**: `2.675` is stored as
`2.67499999…`, and a rounding working on that value would give `2.67`. That is
the "wrong" rounding everyone meets once, and it is also what the workaround
`round($.n * 20) / 20` returns. A zero or negative step **raises** rather than
returning a value that was rounded to nothing; `toprecision` requires at least
one digit. Like `round`, `floor` and `ceil`, all three return a **decimal**.

```jslt
{ "facture": roundhalfup($.n, 2), "caisse": roundto($.n, 0.05), "mesure": toprecision($.n, 3), "bancaire": round($.n, 2) }
```
```json
{ "n": 2.675 }
```
```json
{ "facture": 2.68, "caisse": 2.7, "mesure": 2.68, "bancaire": 2.67 }
```

`toprecision` is for data whose order of magnitude **varies**: `round($.n, 2)`
fixes where the decimal point falls, which makes no sense in a column where
`0.00241` sits next to `24100`.

## Logarithm, bases and non-finite values

| Function | Purpose |
|---|---|
| `log(v, base)` | logarithm in any base (`logarithm` is fixed to e, its variants to 10 and 2) |
| `tobase(v, base, width)` / `frombase(t, base)` | writing in a base from 2 to 36 |
| `isfinite(v)` / `isnan(v)` | is the value a usable number? |

`log(1000, 10)` returns exactly `3.0`: bases 10 and 2 go through their dedicated
function, because dividing two logarithms would return `2.9999999999999996` — and
that number would come straight out in the JSON produced.

`isfinite` serves where JSON is silent: a computation **can** produce infinity
(overflow of a product) while JSON notation cannot write it. Untested, the value
propagates and comes out as `Infinity`, which most readers reject.

`tohex` / `fromhex` remain: they are the special cases written most often, and
they agree with `tobase(v, 16)`.

```jslt
{
  "up": ceil($.v, 2),
  "bits": tobase($.n, 2, 8),
  "read": frombase($.t, 36),
  "usable": isfinite($.v * $.v)
}
```

```json
{ "v": 1.2345, "n": 5, "t": "73" }
```

```json
{ "up": 1.24, "bits": "00000101", "read": 255, "usable": true }
```

---

[← jslt guide](guide.en.md)
