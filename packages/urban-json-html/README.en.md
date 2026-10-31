# urban-json-html

*[Français](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-html/README.md) · English*

[urban-json](https://github.com/gaelgael5/Jslt) plugin: **HTML to JSON** in
templates, through `loadhtml(path_or_url)` (port of .NET's `ServiceHtml`). No
dependency: the standard library's `html.parser`.

```bash
pip install urban-json-html
```

Shape produced (the .NET one, HtmlAgilityPack):

```json
{ "#id": "#document", "content": { "#id": "p", "class": "x", "content": "#text: Hello" } }
```

- element → `{"#id": tag, attributes…, "content": child | [children]}`;
- text → `"#text: …"` (whitespace-only ignored, entities preserved);
- comment and `<!DOCTYPE>` → `"#comment: …"`.

`loadhtml` accepts a file (path or `file://` URI) or an `http(s)://` URL (30 s
timeout). Beware of URLs built from untrusted data (SSRF).
