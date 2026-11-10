# Nombres et maths — guide jslt

*Français · [English](nombres.en.md)*

[← Guide jslt](guide.md) · les exemples de cette page sont **exécutés par la
suite de tests** (`tests/test_guide_examples.py`), sous la forme de triplets
*template → entrée → sortie*.

---

Quirks .NET conservés : `floor`/`round`/`min`/`max` renvoient un **flottant**,
`round` fait un **arrondi bancaire** (0.5 → 0, 1.5 → 2), et `min`/`max` sont
**binaires** (deux arguments).

```jslt
{ "min": min($.a, $.b), "max": max($.a, $.b), "abs": abs($.n), "floor": floor($.d) }
```
```json
{ "a": 2, "b": 8, "n": -5, "d": 2.9 }
```
```json
{ "min": 2.0, "max": 8.0, "abs": 5, "floor": 2.0 }
```

Arrondi bancaire :

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

[← Guide jslt](guide.md)
