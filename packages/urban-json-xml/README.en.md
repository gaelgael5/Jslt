# urban-json-xml

*[Français](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-xml/README.md) · English*

[urban-json](https://github.com/gaelgael5/Jslt) plugin: reading **XML** files from
templates, through the `loadxml` function. Follows the XML↔JSON conventions of
`XmlNodeConverter` (.NET/Newtonsoft).

## Installation

```bash
pip install urban-json-xml      # pulls urban-json and defusedxml as dependencies
```

`urban-json` discovers the plugin automatically through the entry points
(`urban_json.functions`): `loadxml` becomes usable in templates.

## Usage

```python
from urban_json import JsltTemplate

# catalog.xml:
#   <catalog>
#     <book id="1"><title>A</title></book>
#     <book id="2"><title>B</title></book>
#   </catalog>
tpl = JsltTemplate.parse('[ { "$source": select(loadxml("catalog.xml"), $.catalog.book), "t": $.title } ]')
tpl.transform({})
# -> [{'t': 'A'}, {'t': 'B'}]
```

`loadxml` returns an object; you navigate it with `select`/`selectmany` (core
functions) before feeding a `$source` loop, a `?(...)` filter, and so on.

## Conversion conventions (Newtonsoft)

| XML | JSON |
|---|---|
| `<a>v</a>` | `{"a": "v"}` |
| `<a x="1">v</a>` | `{"a": {"@x": "1", "#text": "v"}}` |
| `<a/>` | `{"a": null}` |
| `<a><b>1</b><b>2</b></a>` | `{"a": {"b": ["1", "2"]}}` (same-named siblings → array) |

- Attributes → properties prefixed with `@`.
- Text of a mixed element → `#text` key.
- Values stay **strings** (like Newtonsoft: no coercion).

## Signature

```
loadxml(source_path, attribute_prefix="@", text_key="#text", strip_namespaces=true)
```

| Parameter | Role |
|---|---|
| `source_path` | path to the XML file |
| `attribute_prefix` | prefix for properties built from attributes (default `@`) |
| `text_key` | key carrying the text of a mixed element (default `#text`) |
| `strip_namespaces` | reduces `{uri}local` to the local name (default `true`) |

## Security

XML is parsed with [`defusedxml`](https://pypi.org/project/defusedxml/): external
entities and entity expansion are disabled (XXE and “billion laughs”
protection).

## License

Apache-2.0.
