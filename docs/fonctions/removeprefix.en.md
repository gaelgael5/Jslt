<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `removeprefix`

*[Français](removeprefix.md) · English*

Removes a whole prefix when present, otherwise returns the text unchanged

```
removeprefix(token, prefix)
```

**Example**

*A **whole affix**, where `trimstart` removes a set of characters: on "bacab", `trimstart($.t, "ab")` returns "cab" although the prefix is not there.*

```jslt
{ "present": removeprefix($.t, "ba"), "absent": removeprefix($.t, "ab"), "jeu": trimstart($.t, "ab") }
```

```json
{ "t": "bacab" }
```

```json
{ "present": "cab", "absent": "bacab", "jeu": "cab" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |
| `prefix` | optional |  |

**Chapter**: [Text, regular expressions and formatting](../texte.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
