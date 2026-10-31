# urban-json

*[Français](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json/README.md) · English*

Python port of the **JSLT — JSON Stylesheet Language Transformations** language:
a **template-driven JSON → JSON transformation** language, originally implemented
in .NET ([Black-Beard-Sdk/jslt](https://github.com/Black-Beard-Sdk/jslt)).

This is the **core package** (engine: parser, AST, interpreter, JSONPath, 71
built-in functions, extensibility). Input/output and random generation live in
**separate plugins**, discovered automatically once installed:
`urban-json-csv`, `urban-json-xml`, `urban-json-db`, `urban-json-http`,
`urban-json-elastic`, `urban-json-files`, `urban-json-html`, `urban-json-excel`,
`urban-json-phone`, `urban-json-random`. The editing component
`urban-json-editor` (the `<jslt-editor>` Web Component) is a separate
distribution too.

```python
from urban_json import JsltTemplate

template = JsltTemplate.parse('{ "name": $.user.name, "year": $.user.age + 1 }')
template.transform({"user": {"name": "Alice", "age": 30}})
# -> {'name': 'Alice', 'year': 31}
```

## Installation

```bash
pip install urban-json
```

Single runtime dependency: `antlr4-python3-runtime`. The generated parser is
bundled (no ANTLR tooling, no Java required to *use* the library).

## Documentation

- **Full guide with runnable examples**:
  <https://github.com/gaelgael5/Jslt/blob/main/docs/guide.en.md>
  ([Français](https://github.com/gaelgael5/Jslt/blob/main/docs/guide.md))
- **Project and plugin overview**:
  <https://github.com/gaelgael5/Jslt>

## API

```python
from urban_json import JsltTemplate

tpl = JsltTemplate.parse(source_str)   # compiles (JsltSyntaxError if invalid)
tpl.transform(document)                # applies the template to a document
tpl.debug(document)                     # step-by-step trace (debugging)
tpl.to_source()                        # re-serialises the AST (ToString)
```

Extensibility (adding, isolating and discovering functions, plugins through the
`urban_json.functions` entry points): see the Extensibility section of the guide.

## License

Apache-2.0 (like the original .NET project).
