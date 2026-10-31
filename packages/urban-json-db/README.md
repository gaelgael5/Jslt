# urban-json-db

*Français · [English](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-db/README.en.md)*

Plugin [urban-json](https://github.com/gaelgael5/Jslt) : lecture en **base de données
SQL** depuis les templates. Port de `Bb.Jslt.Services.Sql.ServicesSql` (.NET).

## Installation

```bash
pip install urban-json-db                 # SQLite inclus (stdlib), aucune dépendance en plus
pip install "urban-json-db[postgresql]"   # + connecteur PostgreSQL (psycopg)
pip install "urban-json-db[mysql]"        # + connecteur MySQL (PyMySQL)
```

`urban-json` découvre le plugin automatiquement via les entry points (`urban_json.functions`).

## Utilisation

```python
from urban_json import JsltTemplate

tpl = JsltTemplate.parse('''
{
  "cx:": connectsql("sqlite", "app.db"),
  "users": [ { "$source": readsql(cx:, "SELECT id, name FROM users"), "id": $.id, "n": $.name } ]
}
''')
tpl.transform({})
# -> {"users": [{"id": 1, "n": "Alice"}, ...]}
```

- `connectsql(client, connection)` → descripteur `{client, connection}` (à stocker
  dans une variable).
- `readsql(connection, sql)` → tableau de lignes ; chaque ligne est un objet
  `{"$_line": n, <colonnes...>}` (noms de colonnes assainis, comme en .NET).

## Clients

| Client | Chaîne de connexion | Fourni par |
|---|---|---|
| `sqlite` | chemin du fichier `.db` | stdlib (toujours disponible) |
| `postgresql` | DSN psycopg | extra `postgresql` (à enregistrer) |
| `mysql` | DSN PyMySQL | extra `mysql` (à enregistrer) |

Ajouter un SGBD (connecteur DB-API 2.0) :

```python
import psycopg
from urban_json_db import register_client
register_client("postgresql", psycopg.connect)
```

## Sécurité

`readsql` exécute la requête **telle quelle**. Ne construisez pas le SQL par
concaténation de données non fiables (risque d'injection) : le contenu de `sql`
relève de l'auteur du template.

## Licence

Apache-2.0.
