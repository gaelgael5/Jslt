# urban-json-editor

*[Français](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-editor/README.md) · English*

A reusable **jslt** editing component: a `<jslt-editor>` Web Component with
**syntax highlighting** and **intellisense** (functions **and paths of the
source document**), shipped to be dropped into any Python web project.

- **No browser-side dependency** (vanilla Web Component) → no node build,
  drop-in in an existing project. Since 0.2.0 it is no longer **single-file**:
  `jslt-editor.js` imports `jslt-paths.js` as a module, so the assets must be
  **served** side by side (mount `assets_dir()` as static files). Injecting the
  JS inline in the page fails with `Failed to resolve module specifier
  "./jslt-paths.js"`, for lack of a base URL.
- **Function intellisense** fed by the `urban-json` catalogue
  (`registry.catalog()`), hence always up to date — including the functions of
  installed plugins.
- **Path intellisense** fed either by the **source document** (the `source`
  property: the keys actually present, with their type and a preview of their
  value), or by the **list of paths computed by the host application**
  (`setPaths` / the `paths-url` attribute) when the host knows its input model
  without having an instance of it. The component reads no schema: it folds back
  whatever it is given.

## Installation

```bash
pip install urban-json-editor
```

## Integration (FastAPI)

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import urban_json_editor

app = FastAPI()
urban_json_editor.mount(app, "/jslt-editor")          # serves the JS/CSS assets

@app.get("/api/functions")
def functions():
    return JSONResponse({"functions": urban_json_editor.catalog()})
```

In the page:

```html
<link rel="stylesheet" href="/jslt-editor/jslt-editor.css">
<script type="module" src="/jslt-editor/jslt-editor.js"></script>

<jslt-editor id="ed" catalog-url="/api/functions"></jslt-editor>
<script>
  const ed = document.getElementById("ed");
  ed.value = '{ "n": $.x }';
  ed.source = '{ "x": 1 }';   // source document -> path completion
  ed.addEventListener("input", () => console.log(ed.value));
</script>
```

## Path completion

Two ways to feed the suggestions, one completion engine:

```js
ed.source = '{ "Account": [{ "Name": "ACME" }] }';   // a source document
// or, when the host computes the paths from its input model:
ed.setPaths([
  "$.Account[0].PickupReference",
  { path: "$.Account[0].Name", type: "string", description: "legal name" },
]);
// or, loaded by the component itself:
// <jslt-editor paths-url="/api/source-paths"></jslt-editor>   -> {paths:[…]} or [...]
```

The host's paths **take precedence** over the document when both are supplied
(they describe the model, where a document is only one instance of it). An
invalid source JSON, an empty or missing list: no path suggestions, functions
are still suggested. Triggers:

| Typing | Suggestions |
|---|---|
| `$`, `$.`, `$.user.` | keys of the object reached |
| `$.items.` | keys of the elements, **prefixed with `[*]`** (`$.items.name` is `null` in the engine) |
| `$.items[` | `[*]`, `[0]`, `[1]`… (or the keys, for an object) |
| `$..` | keys at any depth |
| `@.` inside a `[?(…)]` filter | keys of the filtered element |
| `$.` inside a `{ "$source": … }` loop | keys of the **iterated element**, not of the root |

Every suggestion shows the type and a preview of the value (`object · 3 keys`,
`text · "Alice"`…) — or the type **declared** by the host (`string · legal
name`), defaulting to `value`. Subscripts are never invented: a list containing
only `$.Account[0]` will not suggest `[1]`. A key that is not an identifier is
inserted in bracket form (`$.user["home town"]`). No function is suggested
inside a path, and no key is suggested when the path does not resolve: better
nothing than a wrong suggestion.

### Why nothing is suggested (diagnostic messages)

An empty list used to mean six different things: a syntax error, a non-existent
segment, a loop that designates nothing, a missing source document… and also
“you are in the right place, there is nothing below”. The component now tells
them apart, and can say so where the list would have opened.

**Opt-in**: without the attribute, the component stays as silent as in 0.2.x — a
component that suddenly starts talking in every project using it would be a
breaking change.

```html
<jslt-editor hints></jslt-editor>          <!-- or ed.hints = true -->
```

```js
// The texts are overridable by cause CODE (the component carries no i18n
// machinery); a code left alone keeps its shipped text.
ed.setMessages({
  "at-outside-filter": "@ only denotes an element inside a [?(…)] filter",
  "unknown-segment": "{segment} is not in the source document",
});
```

| Code | Situation |
|---|---|
| `no-source-doc` | no source document, or an unreadable one |
| `at-outside-filter` | `@` outside any filter (`{ "a": @. }`) |
| `at-filter-without-brackets` | `@` inside a `?(…)` **without brackets** (the engine rejects it) |
| `unknown-segment` | segment absent from the document (`$.Unknown.`) — data `{segment}` |
| `loop-source-incomplete` | the `$source` path is still being typed |
| `loop-source-empty` | `$source` designating no collection — data `{path}` |
| `filter-path-unknown` | filtered collection that cannot be resolved (`sum($.a)[?(@.`) |
| `filter-path-empty` | filtered collection not found — data `{path}` |
| `no-children` | leaf node: right place, nothing below |
| `no-match` | no key starts with what is typed — data `{prefix}` |

A message **never replaces a list**: it only shows up when no suggestion was
possible, and it does not show up outside a path (it answers a gesture, it does
not comment on typing). It disappears on the next keystroke and on `Escape`,
captures no key, and forbids nothing: the editor informs, it does not validate
the template — saying whether a template compiles remains the engine's job.

## Python API

| Function | Role |
|---|---|
| `assets_dir()` | directory of the static assets (to serve them by hand, outside FastAPI) |
| `catalog(registry=None)` | function catalogue (intellisense) from an urban-json registry |
| `mount(app, url_path="/jslt-editor")` | mounts the assets on a FastAPI/Starlette app |

The assets are `jslt-editor.js`, `jslt-paths.js` (imported by the first one) and
`jslt-editor.css`: serve them side by side (`ASSET_FILES`).

## Component API

- Property `value` (get/set) — the template text (source of truth).
- Property `source` (get/set) / `setSource(doc)` — source document (object,
  array or JSON text) the suggested paths are derived from.
- Property `paths` (get/set) / `setPaths(list)` — paths computed by the host:
  `"$.a[0].b"` or `{path, type, description}`. Take precedence over `source`.
- Attribute `paths-url` — URL to load those paths from (`{paths:[…]}` or `[…]`).
- `setCatalog(list)` — supplies the intellisense catalogue programmatically.
- Attribute `hints` / property `hints` (get/set) — enables the diagnostic
  messages (**default: off**, no message).
- `setMessages(dict)` — texts of the messages by cause code, merged with the
  defaults (`DEFAULT_HINT_MESSAGES`, exported by `jslt-paths.js`).
- Attribute `catalog-url` — URL to load the catalogue from (`{functions:[...]}`).
- Event `input` — emitted on every change.
- Keyboard: while the suggestion list is open, the editor **captures** `Tab`,
  `Enter`, `Escape` and ↑/↓ (`preventDefault`); a host wiring `Enter` or `Tab`
  should test `event.defaultPrevented`. With no list open, `Tab` indents by two
  spaces and other keys reach the host.
- CSS variables `--jslt-ed-*` are overridable (colours, font, height).

## License

Apache-2.0.
