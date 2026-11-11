<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `to_xml`

*[Français](to_xml.md) · English*

Output: the result as XML under the given root element (@key = attribute, #text = content)

```
to_xml(root)
```

**Example**

```jslt
{ "$directives": { "output": { "filter": $.client, "mode": to_xml("client") } }, "client": { "@id": $.id, "ville": $.v } }
```

```json
{ "id": 1, "v": "Lyon" }
```

```json
{ "client": { "@id": 1, "ville": "Lyon" } }
```

`render()` produces:

```text
<?xml version="1.0" encoding="utf-8"?>
<client id="1"><ville>Lyon</ville></client>
```

| Parameter | Expected | Note |
|---|---|---|
| `root` | optional |  |

An **output** function: it is not called in the template body, it is declared in `"$directives": {"output": {"mode": …}}`.

**Chapter**: [Text output](../sortie.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
