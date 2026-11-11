<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `to_json`

*[Français](to_json.md) · English*

Output: serialises the result as JSON, indented when indented is true; ignore_null_and_empty_value drops the null or empty properties

```
to_json(indented, ignore_null_and_empty_value)
```

**Example**

```jslt
{ "$directives": { "output": { "mode": to_json(true) } }, "ville": $.v }
```

```json
{ "v": "Lyon" }
```

```json
{ "ville": "Lyon" }
```

`render()` produces:

```text
{
  "ville": "Lyon"
}
```

| Parameter | Expected | Note |
|---|---|---|
| `indented` | optional |  |
| `ignore_null_and_empty_value` | optional |  |

An **output** function: it is not called in the template body, it is declared in `"$directives": {"output": {"mode": …}}`.

**Good to know**

- `ignore_null_and_empty_value` turns empty strings into `null` **then** removes null properties from objects; arrays keep their elements.

**Chapter**: [Text output](../sortie.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
