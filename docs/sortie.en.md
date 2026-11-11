# Text output — jslt guide

*[Français](sortie.md) · English*

[← jslt guide](guide.en.md) · the examples on this page are **run by the test
suite** (`tests/test_guide_examples.py`) as *template → input → output* triples.

---

A template can declare how its result is **serialized to text**. The
`$directives` key never appears in the result of `transform()`;
`template.render(source)` applies it: `filter` (JSONPath, optional) selects part
of the result (1 node → that node, several → array, none → `null`), then the
output function `mode` produces the text.

```jslt
{ "$directives": { "output": { "filter": $.lignes, "mode": to_block() } },
  "lignes": $.commandes[*] }
```
```json
{ "commandes": [ { "id": 1 }, { "id": 2 } ] }
```
```json
{ "lignes": [ { "id": 1 }, { "id": 2 } ] }
```

Here `render()` yields one JSON line per element (JSON Lines):

```text
{"id":1}
{"id":2}
```

- `to_json(indented, ignore_null_and_empty_value)`: compact JSON, or indented when
  `indented` is `true`; with the 2nd argument, empty strings become `null` and
  null properties are removed from objects.
- `to_block()`: one compact line per array element, or the object on one line.
- Without a directive, `render()` returns the indented JSON of the result.
- Output functions cannot be called in the template body (explicit error); `mode`
  is required. Writing to a file (`write`, `to_file`) or to a database
  (`to_sqlserver`) does not exist: a transformation returns text, and it is up to
  the caller to decide where it goes.

---

## Writing something other than JSON: `to_csv`, `to_xml`, `to_yaml`

The engine can read JSON, XML and CSV from a string (`parsejson`,
[`parsexml`](https://github.com/gaelgael5/Jslt/tree/main/packages/urban-json-xml),
`parsecsv`); it now writes all three. All three emitters are
**dependency-free** — one more dependency in the core is paid at every install —
and follow the reading conventions, so the round trip holds.

| Function | Purpose |
|---|---|
| `to_csv(separator, header)` | array of objects → CSV (RFC 4180), `;` and header by default |
| `to_xml(root)` | document → XML under that root element |
| `to_yaml(json_style)` | document → YAML in block style, or in JSON style |

**CSV.** The columns are the **union of the keys** encountered, in order of
appearance: restricting them to the first object's keys would lose data on a
heterogeneous feed. A missing cell stays empty, which is how a CSV says
"nothing". Nested values are flattened into dotted keys — the same rule as
[`flattenobject`](objets.en.md#deep-structures), since a CSV has no depth. Quotes
are doubled and lines end with CRLF, as the RFC requires.

**XML.** `parsexml` conventions: a key prefixed with `@` becomes an
**attribute**, `#text` the textual content, and a key whose value is an array
**repeats** the element — that is how XML expresses a list. A `null` yields an
empty tag rather than the text "null". An invalid element name raises, because
badly named XML cannot be repaired downstream.

**YAML.** Block style, and an acknowledged subset: no anchors, no tags, no
multi-line literal style. Anything a reader would read back as another type is
**quoted**: the text `"true"`, `"12"` or `"null"` stays text. With
`to_yaml(true)` the output is indented JSON — which is valid YAML, YAML 1.2
being a superset of JSON.

```jslt
{ "$directives": { "output": { "filter": $.rows, "mode": to_csv() } },
  "rows": [ { "$source": $.clients, "id": $.id, "city": $.addr.city } ] }
```

```json
{ "clients": [ { "id": 1, "addr": { "city": "Lyon" } } ] }
```

```json
{ "rows": [ { "id": 1, "city": "Lyon" } ] }
```

`render()` then gives:

```text
id;city
1;Lyon
```

Still not ported: writing to a file (`write` / `to_file`) and `to_sqlserver`, by
decision — a transformation returns text, and where it goes is the caller's call.

---

[← jslt guide](guide.en.md)
