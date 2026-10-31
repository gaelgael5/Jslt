# urban-json-files

*[Français](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-files/README.md) · English*

[urban-json](https://github.com/gaelgael5/Jslt) plugin: **JSON files and paths**
in templates (port of the .NET `loadjson`, `IterateJsonFile` and `concatpath`
functions).

```bash
pip install urban-json-files
```

| Function | Role |
|---|---|
| `loadjson(path)` | Contents of a JSON file (`null` when the file does not exist). |
| `iteratejsonfile(path, "$.path")` | Items of a JSON file selected by a JSONPath (compiled or as a string). |
| `concatpath(["folder", "file.json"])` | Assembled file path (`null` segments ignored; an absolute segment restarts from the root). |

```python
from urban_json import JsltTemplate

tpl = JsltTemplate.parse('{ "ids": iteratejsonfile("data.json", "$.items[*].id") }')
tpl.transform({})
```

Relative paths are relative to the current directory. These functions read the
disk: they are not available in the playground (core-only sandbox).
