# urban-json playground

*[Français](README.md) · English*

A small **test/demo** web application for `urban-json`: you type a jslt template
(in an editor with **syntax highlighting and intellisense**, through the
[`urban-json-editor`](../../packages/urban-json-editor/) component) and a source
JSON document, and you see the result produced by the **real engine**
server-side (FastAPI).

It is not a published distribution — it is an application of this repository.

Features: editor with highlighting and intellisense (functions **and paths of
the source JSON**, triggered on `$` and `@` — the document typed on the right
feeds the suggestions), an **example library**, **automatic transformation**
(debounced, can be turned off), **URL sharing** (the state is encoded in the
link), a **reference panel** of the available functions (filterable), and
**step-by-step debugging** (node-by-node evaluation trace, current source and
value at each step, breakpoints on functions).

## Running locally

```bash
pip install -e "apps/playground[dev]"      # pulls urban-json, urban-json-editor, fastapi, uvicorn
uvicorn urban_json_playground.app:app --reload
# then http://127.0.0.1:8000
```

## Security

The playground runs **core functions only**. The I/O plugins (CSV, XML, SQL,
HTTP, Elasticsearch) are **not** loaded: an arbitrary template can therefore
neither read the server's files, nor issue requests (SSRF), nor run SQL.
Technically, an isolated registry (a copy of the core registry, without plugins)
is passed to every `transform`.

The application is not hardened for public hosting (no rate limit, no execution
timeout); add those guards before exposing it.

## Endpoints

| Method | Path | Role |
|---|---|---|
| `POST` | `/api/transform` | `{template, source}` → `{result}` or `{error}` |
| `POST` | `/api/debug` | `{template, source, break_functions, break_lines}` → `{result, steps, error}` |
| `GET` | `/api/functions` | function catalogue (core) for intellisense |
| `GET` | `/api/examples` | ready-to-load examples (template + source) |
| `GET` | `/jslt-editor/*` | assets of the editing component |
| `GET` | `/` | the playground page |

## License

Apache-2.0.
