# urban-json-csv

*[Français](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-csv/README.md) · English*

[urban-json](https://github.com/gaelgael5/Jslt) plugin: reading **CSV** files from
templates, through the `loadcsv` function. Port of
`Bb.CustomServices.ServiceCsv` (.NET).

## Installation

```bash
pip install urban-json-csv      # pulls urban-json as a dependency
```

Nothing else to do: `urban-json` discovers the plugin automatically through the
entry points (`urban_json.functions`), and `loadcsv` becomes usable in templates.

## Usage

```python
from urban_json import JsltTemplate

# people.csv:
#   name;age;active
#   Alice;30;true
#   Bob;25;false
tpl = JsltTemplate.parse('[ { "$source": loadcsv("people.csv"), "n": $.name, "a": $.age } ]')
tpl.transform({})
# -> [{'n': 'Alice', 'a': 30}, {'n': 'Bob', 'a': 25}]
```

`loadcsv` returns an array of objects (one entry per row), so it chains naturally
into a `$source` loop, a `?(...)` filter, and so on.

## Signature

```
loadcsv(source_path, has_header=true, separator=";", quote="\"", escape="\\",
        excluded_columns=null, exclude_null_and_empty=false)
```

| Parameter | Role |
|---|---|
| `source_path` | path to the CSV file (absolute, or relative to the current directory) |
| `has_header` | the first row carries the column names (otherwise `Column0`, `Column1`…) |
| `separator` | field separator (default `;`) |
| `quote` | quoting character (default `"`) |
| `escape` | escape character (default `\`) |
| `excluded_columns` | names of columns to drop, separated by `separator` |
| `exclude_null_and_empty` | omits null and empty cells |

### From a string: `parsecsv`

```
parsecsv(text, has_header=true, separator=";", quote="\"", escape="\\",
         excluded_columns=null, exclude_null_and_empty=false)
```

The same options and the same cell typing, but on CSV **already in hand**: a
message, an archive, a database column. `null` stays `null`; a non-text argument
raises `JsltError` (the engine's family, catchable by `trydefault`).

### Value typing

Cells are **typed** on reading: `true`/`false` → boolean, integers and decimals →
numbers, anything else → string (headers are sanitised: accents → ASCII, spaces
→ `_`).

## `loadmcsv` — hierarchical multi-record CSV

Port of `ServicesMultiCsv`: a `;`-delimited file where every line is prefixed by
a **record type**, each type's columns being declared by `#DEF` lines. A
`rule_payload` describes the **hierarchy**.

```
#DEF;CATALOG;id;name
#DEF;BOOK;code;title
CATALOG;1;Bookshop
BOOK;a;Alpha
BOOK;b;Beta
#END
```

```python
from urban_json import JsltTemplate
JsltTemplate.parse(
    '[ { "$source": selectmany(loadmcsv("catalog.mcsv", "CATALOG:BOOK"), $.BOOK.*), "t": $.title } ]'
).transform({})
# -> [{'t': 'Alpha'}, {'t': 'Beta'}]
```

`loadmcsv(source_path, rule_payload, encoding, ignore_empty)`:
- `rule_payload`: rules `"PARENT:CHILD1|CHILD2; …"` (separated by `;`). A block
  whose name is a child of the current parent nests into it, otherwise it pops up.
- Same-named children become an **array**; every root carries a `_metadatas`
  object (file name, encoding, `#key` metadata from the file).
- Lines `#DEF;<schema>:<NAME>;col…` (columns), `#key;…` (metadata), `#END` (end).

Reading choices: `utf-8` encoding; column mapping **by position**, tolerant to
one trailing `;` too many; type names compared in upper case.

## License

Apache-2.0.
