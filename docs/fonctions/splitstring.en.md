<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `splitstring`

*[Français](splitstring.md) · English*

Cuts a text on a whole separator (several characters), at most limit times

```
splitstring(token, separator, limit)
```

**Examples**

*A **whole** separator, where `split` only keeps its 1st character.*

```jslt
{ "entier": splitstring($.t, " - "), "premier_caractere": split($.t, " - ") }
```

```json
{ "t": "a - b - c" }
```

```json
{ "entier": ["a", "b", "c"], "premier_caractere": ["a", "-", "b", "-", "c"] }
```

*`limit` counts the **cuts**: `1` returns two elements, the rest of the text being kept whole.*

```jslt
{ "une_coupe": splitstring($.t, ",", 1) }
```

```json
{ "t": "a,b,c" }
```

```json
{ "une_coupe": ["a", "b,c"] }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `separator` | optional |  |
| `limit` | optional |  |

**Good to know**

- `limit` is the number of **cuts**, not of pieces: with `1` you get two elements and the rest of the text is kept whole.

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
