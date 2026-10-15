# jslt (Python)

*[Français](README.md) · English*

Python port of the **JSLT — JSON Stylesheet Language Transformations** language:
a **template-driven JSON → JSON transformation** language, originally implemented
in .NET ([Black-Beard-Sdk/jslt](https://github.com/Black-Beard-Sdk/jslt)).

A template **describes the shape of the target JSON**; its values are expressions
that read the source document: JSONPath paths (`$.x`), variables (`var:`),
functions (`sum(...)`), operators (`+`, `==`, `??`…), loops
(`[ { "$source": $.items } ]`), conditionals (`when`), casts (`#integer`).

```python
from jslt import JsltTemplate

template = JsltTemplate.parse('{ "name": $.user.name, "year": $.user.age + 1 }')
template.transform({"user": {"name": "Alice", "age": 30}})
# -> {'name': 'Alice', 'year': 31}
```

## Installation

```bash
pip install -e ".[dev]"   # from the repo; also installs pytest + ruff
```

The only runtime dependency is `antlr4-python3-runtime`. The generated parser is
**checked into version control**: no ANTLR tooling (nor Java) is needed to *use*
the library — only to *regenerate* the parser after changing the grammars.

## At a glance

| Capability | Template example | Source | Result |
|---|---|---|---|
| Constants / structure | `{ "v": "Paris" }` | `{}` | `{"v": "Paris"}` |
| JSONPath | `{ "n": $.user.name }` | `{"user":{"name":"A"}}` | `{"n": "A"}` |
| Recursive descent | `{ "ids": $..id }` | `{"a":{"id":1},"b":{"id":2}}` | `{"ids":[1,2]}` |
| Variables | `{ "u:": $.user, "n": u:$.name }` | `{"user":{"name":"B"}}` | `{"n":"B"}` |
| Operators | `{ "s": $.a + $.b }` | `{"a":1,"b":2}` | `{"s":3}` |
| Coalescing | `{ "v": $.x ?? "def" }` | `{}` | `{"v":"def"}` |
| Functions | `{ "t": sum($.n) }` | `{"n":[1,2,3]}` | `{"t":6}` |
| Casts | `{ "i": $.s #integer }` | `{"s":"42"}` | `{"i":42}` |
| `when` / `switch` | `{ "r": when($.x) { "a": 1, "default": 0 } }` | `{"x":"a"}` | `{"r":1}` |
| Loops | `[ { "$source": $.u, "n": $.name } ]` | `{"u":[{"name":"A"}]}` | `[{"n":"A"}]` |
| JSONPath filters | `{ "g": $.items[?(@.n > 1)] }` | `{"items":[{"n":1},{"n":2}]}` | `{"g":[{"n":2}]}` |

The **[full guide with many runnable examples](docs/guide.en.md)** covers every
construct in detail. All of its examples are executed by the test suite
(`tests/test_guide_examples.py`), so they can never go stale.

## Public API

```python
from jslt import JsltTemplate

tpl = JsltTemplate.parse(source_str)   # compile the template (raises JsltSyntaxError if invalid)
tpl.transform(document)                # apply the template to a document (dict/list/scalar)
tpl.to_source()                        # re-serialize the AST to a re-parseable template (ToString)
tpl.ast                                # the AST (tree of JsltBase nodes)
```

Exceptions: `JsltError` (base), `JsltSyntaxError` (parsing), `JsltSemanticError`.
Constructs recognized by the grammar but not yet ported raise `NotImplementedError`
with an explicit message (never a wrong result).

## Extensibility (functions & plugins)

Add a function usable in templates, isolate a set of functions, introspect the
registry, or consume third-party plugins — the idiomatic Python equivalent of
.NET's service mechanism:

```python
from jslt import jslt_function, JsltTemplate, default_registry

@jslt_function("double", description="Doubles a number")
def _double(ctx, x=None):
    return x * 2

JsltTemplate.parse('{ "r": double($.n) }').transform({"n": 21})   # -> {'r': 42}
default_registry.names()          # discovery: list of available functions
default_registry.describe("double").signature()   # 'double(x)'
```

**Third-party plugins** are auto-discovered via the `jslt.functions` entry point
group (installing the package is enough). Details and the plugin contract in the
[guide, §Extensibility](docs/guide.en.md#16-extensibility-functions-and-plugins).

**Official plugins** (monorepo, separate distributions):
- [`jslt-csv`](packages/jslt-csv/) — reading CSV files (`loadcsv`).
- [`jslt-xml`](packages/jslt-xml/) — reading XML files (`loadxml`).
- [`jslt-db`](packages/jslt-db/) — reading from SQL databases (`connectsql`, `readsql`).
- [`jslt-http`](packages/jslt-http/) — HTTP calls (`http`, `httpget`).

## Architecture

The pipeline mirrors the .NET engine, **without** its code
generation / compilation stage (Roslyn): in Python the transformation is carried
out by an **AST interpreter** (tree-walking), simpler and more portable, with
identical behavior.

```
template text
  └─ ANTLR parser (grammar grammar/*.g4)        src/jslt/_antlr/ (generated, versioned)
       └─ ANTLR parse tree
            └─ ScriptBuilderVisitor               src/jslt/parsing/ (ANTLR tree → AST)
                 └─ AST (Visitor pattern)         src/jslt/ast/
                      └─ interpreter (tree-walk)   src/jslt/runtime/
                           ├─ JSONPath             src/jslt/jsonpath/ (port of Bb.JPaths, RFC 9535)
                           └─ functions            src/jslt/functions/ (registry by name)
```

Patterns carried over from .NET, notably the **double-dispatch Visitor** (each
`JsltBase` node has `accept(visitor)` calling `visitor.visit_xxx(self)`, mapped
1:1 to the .NET names) and the **two visitor layers** (AST construction, then
evaluation and serialization). Details and deliberate deviations in
[`CLAUDE.md`](CLAUDE.md) (in French).

## Development

```bash
pip install -e ".[dev]"
pytest                       # test suite
ruff check src tests         # lint (generated _antlr/ is excluded)
bash scripts/generate_parser.sh   # regenerate the parser after editing grammar/*.g4 (Java required)
```

The grammar is authoritative: `grammar/JsltLexer.g4` and `grammar/JsltParser.g4`
are the language's source of truth, taken from the .NET repository.

## Scope

The port targets the engine's **core**. Out of scope (extensible): some
set-membership filter operators (`nin`/`subsetof`/`contains`…, also absent from
.NET), I/O functions (`csv`, `http`, `sql`…) and joins (`group`, `join`, `index`).
The list of ported functions and the assumed deviations from .NET are documented
in [`CLAUDE.md`](CLAUDE.md).

## License

Apache-2.0 (like the original .NET project).
