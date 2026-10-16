# urban-json-elastic

Plugin [urban-json](https://github.com/gaelgael5/Jslt) : recherche **Elasticsearch**
depuis les templates, via le client officiel `elasticsearch`.

## Installation

```bash
pip install urban-json-elastic      # tire urban-json et le client elasticsearch
```

`urban-json` découvre le plugin automatiquement via les entry points (`urban_json.functions`).

## Utilisation

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

- `esconnect(hosts, api_key, username, password, verify_certs)` → descripteur de
  connexion (à stocker dans une variable).
- `essearch(connection, index, query, size)` → liste des documents trouvés
  (le `_source` de chaque hit). `query` est une clause du DSL Elasticsearch
  (`match_all` si absente).

## Sécurité

`essearch` interroge un cluster Elasticsearch réel. Les identifiants (api_key /
mot de passe) transitent par le descripteur de connexion : traitez-les comme des
secrets côté template.

## Licence

Apache-2.0.
