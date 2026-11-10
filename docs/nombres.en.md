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

[← jslt guide](guide.en.md)
