<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `to_yaml`

*[Français](to_yaml.md) · English*

Output: the result as YAML, in block style or in JSON style when json_style is true

```
to_yaml(json_style)
```

**Example**

```jslt
{ "$directives": { "output": { "filter": $.client, "mode": to_yaml() } }, "client": { "id": $.id, "ville": $.v } }
```

```json
{ "id": 1, "v": "Lyon" }
```

```json
{ "client": { "id": 1, "ville": "Lyon" } }
```

`render()` produces:

```text
id: 1
ville: Lyon
```

| Parameter | Expected | Note |
|---|---|---|
| `json_style` | optional |  |

An **output** function: it is not called in the template body, it is declared in `"$directives": {"output": {"mode": …}}`.

**Good to know**

- An acknowledged subset: no anchors, no tags, no multi-line literal. Any scalar that would read back as another type is **quoted** — a `"true"` or `"12"` text stays text.

**Chapter**: [Text output](../sortie.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
