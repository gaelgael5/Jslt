<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `ifelse`

*[Français](ifelse.md) · English*

Value of the 2nd expression when the condition is true, otherwise that of the 3rd (only the chosen branch is evaluated)

```
ifelse(condition, when_true, when_false)
```

**Example**

*The branch left aside is **not** evaluated: the division by zero does not run.*

```jslt
{ "taille": ifelse($.n > 10, "grand", "petit"), "ratio": ifelse($.d == 0, 0, 100 / $.d) }
```

```json
{ "n": 42, "d": 0 }
```

```json
{ "taille": "grand", "ratio": 0 }
```

| Parameter | Expected | Note |
|---|---|---|
| `condition` | optional | the expression to test; read like `filter`'s (`null`, `0`, `""`, empty = false), not like an assertion |
| `when_true` | optional | value returned when the condition is true; **not evaluated** otherwise · **unevaluated** expression, computed by the function |
| `when_false` | optional | value returned otherwise; absent, the result is `null` · **unevaluated** expression, computed by the function |

**Good to know**

- Only the **chosen** branch is evaluated: `ifelse($.d == 0, 0, 100 / $.d)` does not divide by zero. That is the whole point of the function, and what an operator with evaluated arguments could not offer.
- `when` switches on a **value** (`==` against each case name); `ifelse` tests a **condition**, hence a composed expression. For more than two cases, `ifelse` nests.

**Chapter**: [Conditionals and loops](../conditions-et-boucles.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
