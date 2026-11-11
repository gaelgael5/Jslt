# Numbers and math — jslt guide

*[Français](nombres.md) · English*

[← jslt guide](guide.en.md) · the examples on this page are **run by the test
suite** (`tests/test_guide_examples.py`) as *template → input → output* triples.

---

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

[← jslt guide](guide.en.md)
