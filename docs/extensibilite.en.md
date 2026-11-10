# Extensibility, debugging and re-serialization — jslt guide

*[Français](extensibilite.md) · English*

[← jslt guide](guide.en.md) · the examples on this page are **run by the test
suite** (`tests/test_guide_examples.py`) as *template → input → output* triples.

---

## Extensibility: functions and plugins

You can **add** your own functions, **isolate** them, **discover** them, and
consume installed **third-party plugins** — the idiomatic Python equivalent of
.NET's service mechanism.

### Adding a function

```python
from urban_json import jslt_function, JsltTemplate

@jslt_function("double", description="Doubles a number")
def _double(ctx, x=None):
    return x * 2

JsltTemplate.parse('{ "r": double($.n) }').transform({"n": 21})   # -> {'r': 42}
```

A function always receives the execution context as its first parameter (`ctx`),
then the template arguments. `path_args=(indices)` marks arguments received as a
compiled (unevaluated) JSONPath, as for `distinct`.

### Isolating a set of functions

A dedicated registry lets you limit/isolate the available functions (sandbox):

```python
from urban_json import FunctionRegistry, default_registry, JsltTemplate

sandbox = FunctionRegistry()                      # empty: no built-in functions
sandbox.register("triple", lambda ctx, x=None: x * 3)
JsltTemplate.parse('{ "r": triple($.n) }').transform({"n": 7}, functions=sandbox)

# Start from the built-ins without mutating the global registry:
derived = default_registry.copy()
derived.register("triple", lambda ctx, x=None: x * 3)
```

### Discovering available functions

```python
from urban_json import default_registry

default_registry.names()                 # ['abs', 'concat', 'distinct', ...]
info = default_registry.describe("distinct")
info.signature()                         # 'distinct(source, path)'
info.path_args                           # (1,)
info.description                         # first docstring line
info.parameters[1].name, info.parameters[1].type, info.parameters[1].is_path
#                                        # ('path', 'Any', True)
```

To feed a **template editor** (auto-completion, contextual help), `catalog()`
returns a **JSON-serializable** list describing every function (name, description,
parameters name + type + required + path, return type, signature):

```python
import json
from urban_json import default_registry

json.dumps(default_registry.catalog())   # ready to hand to an editor
# [{"name": "distinct", "description": "...", "signature": "distinct(source, path)",
#   "parameters": [{"name": "source", "type": "Any", "required": false, ...},
#                  {"name": "path", "type": "Any", "is_path": true, ...}],
#   "returns": "list", "path_args": [1]}, ...]
```

### Third-party plugins (entry points)

An installed package exposes its functions by declaring the `urban_json.functions` entry
point group. On the plugin side, in its `pyproject.toml`:

```toml
[project.entry-points."urban_json.functions"]
my_package = "my_package.jslt_ext:register"
```

with a `register` function that registers into the given registry:

```python
def register(registry):
    registry.register("shout", lambda ctx, s=None: (s or "").upper() + "!")
```

Plugins are discovered **automatically** on the first `transform` (or on demand via
`load_plugins()`), then usable in templates like the built-in functions. This is
the mechanism intended for the additional packages (I/O: CSV, databases,
Elasticsearch…).

---

## Debugging (step-by-step)

`JsltTemplate.debug(source)` evaluates the template while collecting a
**step-by-step trace**: one step per evaluated node, with its location, the current
source and the produced value. (The engine is an interpreter, so debugging happens
at the template level — there is no generated code as in .NET.)

```python
from urban_json import JsltTemplate

r = JsltTemplate.parse('{ "t": sum($.n) }').debug({"n": [1, 2, 3]})
r.result                      # {'t': 6}
for step in r.steps:
    print(step.kind, step.line, step.expression, "->", step.result)
# JsltPath 1 $.n -> [1, 2, 3]
# JsltFunctionCall 1 sum(…) -> 6
# JsltObject 1 None -> {'t': 6}
```

**Breakpoints**: flag the steps matching a function ("context method") or a template
line.

```python
r = JsltTemplate.parse('{ "t": sum($.n) }').debug({"n": [1, 2]}, break_functions=["sum"])
[s.expression for s in r.steps if s.breakpoint]   # ['sum(…)']
```

`DebugResult` carries `result` (final value), `steps` (list of `TraceStep`) and
`error` (message if evaluation fails — the partial trace is still available). The
playground (`apps/playground`) offers a visual step-through.

---

## Re-serialization `to_source()`

`JsltTemplate.to_source()` rebuilds a **valid, re-parseable** template from the AST
(analogous to .NET's `ToString`). The result is equivalent in **behavior** (not
necessarily identical character-for-character); a `#type` cast reappears in its
`convert(x, "type")` form.

```python
from urban_json import JsltTemplate

tpl = JsltTemplate.parse('{ "sum": $.a + $.b }')
tpl.to_source()                          # -> '{ "sum": $.a + $.b }'
JsltTemplate.parse(tpl.to_source())      # re-parseable without error
```


---

[← jslt guide](guide.en.md)
