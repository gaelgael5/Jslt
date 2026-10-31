# urban-json-db

*[Français](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-db/README.md) · English*

[urban-json](https://github.com/gaelgael5/Jslt) plugin: reading from a **SQL
database** in templates. Port of `Bb.Jslt.Services.Sql.ServicesSql` (.NET).

## Installation

```bash
pip install urban-json-db                 # SQLite included (stdlib), no extra dependency
pip install "urban-json-db[postgresql]"   # + PostgreSQL connector (psycopg)
pip install "urban-json-db[mysql]"        # + MySQL connector (PyMySQL)
```

`urban-json` discovers the plugin automatically through the entry points
(`urban_json.functions`).

## Usage

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

- `connectsql(client, connection)` → a `{client, connection}` descriptor (to be
  stored in a variable).
- `readsql(connection, sql)` → an array of rows; each row is an object
  `{"$_line": n, <columns...>}` (column names sanitised, as in .NET).

## Clients

| Client | Connection string | Provided by |
|---|---|---|
| `sqlite` | path to the `.db` file | stdlib (always available) |
| `postgresql` | psycopg DSN | `postgresql` extra (to be registered) |
| `mysql` | PyMySQL DSN | `mysql` extra (to be registered) |

Adding a DBMS (any DB-API 2.0 connector):

```python
import psycopg
from urban_json_db import register_client
register_client("postgresql", psycopg.connect)
```

## Security

`readsql` runs the query **as is**. Do not build SQL by concatenating untrusted
data (injection risk): the content of `sql` is the template author's
responsibility.

## License

Apache-2.0.
