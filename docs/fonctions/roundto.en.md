<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `roundto`

*[Français](roundto.md) · English*

Rounds to the nearest multiple (roundto(2.34, 0.05) -> 2.35), halves away from zero

```
roundto(token, step)
```

**Example**

```jslt
{ "caisse": roundto($.n, 0.05), "quart_heure": roundto($.m, 15) }
```

```json
{ "n": 2.34, "m": 38 }
```

```json
{ "caisse": 2.35, "quart_heure": 45.0 }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `step` | optional | the rounding step, strictly positive (`0.05`, `15`, `0.25`); zero or negative, it raises |

**Good to know**

- A zero or negative step **raises**, rather than returning a value that was rounded to nothing — which a `roundto($.n, $.step)` with a missing step would produce.
- Halves go away from zero, like `roundhalfup`, and the computation goes through no intermediate float: the workaround `round($.n * 20) / 20` did, with the representation error that comes with it.

**Chapter**: [Numbers and maths](../nombres.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
