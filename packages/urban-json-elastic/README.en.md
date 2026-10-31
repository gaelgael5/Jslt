# urban-json-elastic

*[Français](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-elastic/README.md) · English*

[urban-json](https://github.com/gaelgael5/Jslt) plugin: **Elasticsearch** search
from templates, through the official `elasticsearch` client.

## Installation

```bash
pip install urban-json-elastic      # pulls urban-json and the elasticsearch client
```

`urban-json` discovers the plugin automatically through the entry points
(`urban_json.functions`).

## Usage

```python
from urban_json import JsltTemplate

tpl = JsltTemplate.parse('''
{
  "es:": esconnect("https://localhost:9200", $.api_key),
  "docs": [ {
    "$source": essearch(es:, "products", { "match": { "category": "book" } }, 50),
    "nom": $.title, "prix": $.price
  } ]
}
''')
```

- `esconnect(hosts, api_key, username, password, verify_certs)` → a connection
  descriptor (to be stored in a variable).
- `essearch(connection, index, query, size)` → the list of matching documents
  (the `_source` of each hit). `query` is an Elasticsearch DSL clause
  (`match_all` when omitted).

## Security

`essearch` queries a real Elasticsearch cluster. Credentials (api_key or
password) travel through the connection descriptor: treat them as secrets on the
template side.

## License

Apache-2.0.
