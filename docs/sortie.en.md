# Text output — jslt guide

*[Français](sortie.md) · English*

[← jslt guide](guide.en.md) · the examples on this page are **run by the test
suite** (`tests/test_guide_examples.py`) as *template → input → output* triples.

---

As in .NET, a template can declare how its result is **serialized to text**. The
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
  is required. The .NET writer functions (`write`, `to_file`) and `to_sqlserver`
  are not ported.

---

[← jslt guide](guide.en.md)
