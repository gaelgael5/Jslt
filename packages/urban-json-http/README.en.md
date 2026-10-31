# urban-json-http

*[Français](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-http/README.md) · English*

[urban-json](https://github.com/gaelgael5/Jslt) plugin: **HTTP** calls from
templates. A call is expressed as a **Fetch / `RequestInit`** object (the
standard HTTP-in-JSON vocabulary).

## Installation

```bash
pip install urban-json-http      # pulls urban-json and httpx
```

`urban-json` discovers the plugin automatically through the entry points
(`urban_json.functions`).

## Usage

```python
from urban_json import JsltTemplate

tpl = JsltTemplate.parse('''
{
  "r:": http({
    "method": "GET",
    "url": "https://api.example.com/users",
    "headers": { "Authorization": $.token },
    "query": { "page": 1 }
  }),
  "code": r:$.status,
  "users": r:$.body.items
}
''')
tpl.transform({"token": "Bearer xyz"})
```

- `http(request)` — `request`: `{ method, url, headers, query, body, timeout }`.
  Returns `{ status, headers, body }`; `body` is the parsed JSON when the
  response is JSON, otherwise the text.
- `httpget(url, headers)` — GET convenience returning the `body` directly.

The request `body` is sent as **JSON** when it is an object or an array,
otherwise as is. Default verb: `GET`. Default timeout: 30 s (override with
`"timeout"`).

## Security

`http` performs **real network requests**. Beware of URLs built from untrusted
data (SSRF). A default timeout is applied.

## License

Apache-2.0.
