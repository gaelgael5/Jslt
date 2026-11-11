<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `walk`

*[Français](walk.md) · English*

Applies an expression to every node of a structure, from the leaves to the root

```
walk(token, expression)
```

**Example**

```jslt
{ "r": walk($.o, when(isstring($)) { "True": upper($), "default": $ }) }
```

```json
{ "o": { "a": "x", "b": { "c": "y" } } }
```

```json
{ "r": { "a": "X", "b": { "c": "Y" } } }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `expression` | optional | **unevaluated** expression, computed by the function |

**Good to know**

- The walk goes from the **leaves to the root**: the expression sees already transformed children, so a rule that depends on them works.

**Chapter**: [Objects and deep structures](../objets.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
