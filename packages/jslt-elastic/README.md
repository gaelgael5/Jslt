# jslt-elastic

Plugin [jslt](https://github.com/gaelgael5/Jslt) : recherche **Elasticsearch**
depuis les templates, via le client officiel `elasticsearch`.

## Installation

```bash
pip install jslt-elastic      # tire jslt et le client elasticsearch
```

`jslt` découvre le plugin automatiquement via les entry points (`jslt.functions`).

## Utilisation

```python
from jslt import JsltTemplate

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
