# Embedding the engine — jslt guide

*[Français](integration.md) · English*

[← jslt guide](guide.en.md) · this page documents the engine's **hook points**
for an application that embeds it, and the level of guarantee each one carries.

---

## Three surfaces, three guarantees

| Surface | Import | Guarantee |
|---|---|---|
| **Public API** | `from urban_json import …` (everything in `__all__`) | **stable**. A break goes through a minor or major version, announced in the [CHANGELOG](../CHANGELOG.en.md). |
| **Documented internals** | `urban_json.parsing`, `urban_json.runtime`, `urban_json.ast`, `urban_json.jsonpath` | **documented, not frozen**. These names exist and do what is written here; a move or a signature change is **announced in the CHANGELOG**, without waiting for a major version. |
| **Undocumented internals** | everything else: modules and functions prefixed `_`, `urban_json._antlr` (generated), the helpers under `functions/` | **no guarantee**, may change in any version. |

**Why this page exists.** An integration relied on `parse_to_tree`,
`ScriptBuilderVisitor`, `JsltEvaluationVisitor`, `RuntimeContext`, `Sources`,
`JsltKind` and the JSONPath selectors — with no documentation saying whether
those names were stable. Lacking a contract, the upgrade had to be validated by
**comparing the sources of two versions byte for byte** to establish that
`parsing/`, `ast/`, `runtime/` and `jsonpath/` had not moved. That is the cost of
an undocumented surface: the burden of the guarantee falls on the integrator, at
every version. The middle row exists for that, and the CHANGELOG serves it.

## The ordinary path

```python
from urban_json import JsltTemplate

template = JsltTemplate.parse(template_text)      # -> AST, raises JsltSyntaxError
result = template.transform(document)              # -> Python structures
text = template.render(document)                   # -> text ($directives.output)
```

- `transform(source, functions=…, parameters=…)`: `functions` isolates the set of
  available functions, `parameters` passes settings read by `param("name")`.
- `build()` switches on the compiled path (×3 to ×5 in bulk); the result is
  **identical** to the interpreter, verified on every example in the guide.
- `debug(...)` returns a step-by-step trace, `to_source()` re-serialises the AST.

## The pipeline, piece by piece

```
text  ──parse_to_tree──▶  ANTLR tree  ──ScriptBuilderVisitor──▶  AST
                                                                  │
                                            JsltEvaluationVisitor │ (+ RuntimeContext)
                                                                  ▼
                                                               result
```

| Piece | Import | Purpose |
|---|---|---|
| `parse_to_tree(text)` | `urban_json.parsing` | ANTLR parse tree (`script` rule); raises `JsltSyntaxError` with `line` / `column` |
| `ScriptBuilderVisitor` | `urban_json.parsing` | ANTLR tree → jslt AST (`.visit(tree)`) |
| `JsltBase`, `JsltKind` | `urban_json.ast` | AST nodes and their nature (`JsltKind` is 1:1 with the .NET enum) |
| `JsltJsonVisitor`, `JsltBaseVisitor` | `urban_json.ast` | double-dispatch visitor; `JsltBaseVisitor` descends by default, you override the `visit_*` you care about |
| `Sources`, `RuntimeContext` | `urban_json.runtime` | source documents / execution state (current-source stack, variables, `parameters`, `token_result`) |
| `JsltEvaluationVisitor` | `urban_json.runtime` | AST interpreter (`ast.accept(visitor)`) |
| `Program`, `compile_program` | `urban_json.runtime` | the compiled path (closures) behind `build()` |
| `JsonPath`, `PathScope`, `Node` | `urban_json.jsonpath` | compiled path: `evaluate(root)` returns `Node`s, `select_values(root)` their values |
| `ISelector` and its classes | `urban_json.jsonpath` | one selector per construct (`NameSelector`, `IndexSelector`, `SliceSelector`, `WildcardSelector`, `FilterSelector`, `PathFunctionSelector`) |

The full pipeline by hand — useful to inspect the tree between two stages, or to
supply a prepared context:

```python
from urban_json.parsing import ScriptBuilderVisitor, parse_to_tree
from urban_json.runtime import JsltEvaluationVisitor, RuntimeContext, Sources

ast = ScriptBuilderVisitor().visit(parse_to_tree('{ "a": $.x + 1, "batch": param("batch") }'))
context = RuntimeContext(Sources({"x": 2}), None, {"batch": "A-12"})
ast.accept(JsltEvaluationVisitor(context))      # {'a': 3, 'batch': 'A-12'}
```

`RuntimeContext(sources, functions, parameters)`: `functions` set to `None` uses
the global registry. All three arguments are positional and optional.

## Tooling a template without running it

The AST is walked with a visitor. To inventory the functions a template calls —
auditing, editor assistance, statistics:

```python
from urban_json import JsltTemplate
from urban_json.ast import JsltBaseVisitor, JsltFunctionCall

class FunctionNames(JsltBaseVisitor):
    def __init__(self):
        self.names = set()

    def visit_function(self, node: JsltFunctionCall):
        self.names.add(node.name)
        return super().visit_function(node)   # keep descending

visitor = FunctionNames()
JsltTemplate.parse('{ "a": upper($.x), "b": sort($.l, foldtext($)) }').ast.accept(visitor)
sorted(visitor.names)      # ['foldtext', 'sort', 'upper']
```

**To allow or refuse functions, do not stop there.** An AST inventory answers
"which functions does this text name"; it does not guarantee "which functions the
run will be able to reach". The reliable guard is a **dedicated registry**,
because that is what the engine consults at run time:

```python
from urban_json import JsltTemplate, default_registry

sandbox = default_registry.copy()          # independent copy of the global registry
for name in ("http", "readsql", "loadjson"):
    sandbox.remove(name)                   # returns False if it was not there
JsltTemplate.parse(text).transform(document, functions=sandbox)
```

That is what this repository's playground does: isolated registry, core functions
only, no I/O from a template. An AST inventory is for **explaining** a refusal;
the registry is what **holds** it.

For editor assistance, `registry.catalog()` returns a JSON-serialisable list
(name, description, typed parameters, return, signature, `path_args`,
`lazy_args`), and `describe(name)` a `FunctionInfo`.

## What is not an API

- `urban_json._antlr/`: code **generated** by ANTLR, versioned so the library can
  be used without the tool. The grammar (`grammar/*.g4`) is authoritative.
- `functions/_helpers.py`, `functions/_dateread.py`, `functions/_datecalc.py`,
  `functions/_schemacheck.py`: internal helpers, named `_` for that reason.
- The internals of `functions/formatting.py` (culture tables, mask tokens):
  reused **inside** the package by date and number reading, not meant for
  outside use.

To add functions, the extension point is documented:
[Extensibility](extensibilite.en.md) (the `@jslt_function` decorator, the
registry, entry-point plugins).

---

**See also**: [CHANGELOG](../CHANGELOG.en.md) for what moved between versions,
[`CLAUDE.md`](../CLAUDE.md) (in French) for the architecture and the deliberate
deviations from .NET.

---

[← jslt guide](guide.en.md)
