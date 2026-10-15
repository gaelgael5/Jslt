# jslt (Python)

*Français · [English](README.en.md)*

Portage Python du langage **JSLT — JSON Stylesheet Language Transformations** :
un langage de **transformation JSON → JSON piloté par template**, initialement
implémenté en .NET ([Black-Beard-Sdk/jslt](https://github.com/Black-Beard-Sdk/jslt)).

Un template décrit la **forme du JSON cible** ; ses valeurs sont des expressions
qui lisent le document source : chemins JSONPath (`$.x`), variables (`var:`),
fonctions (`sum(...)`), opérateurs (`+`, `==`, `??`…), boucles
(`[ { "$source": $.items } ]`), conditions (`when`), casts (`#integer`).

```python
from jslt import JsltTemplate

template = JsltTemplate.parse('{ "name": $.user.name, "year": $.user.age + 1 }')
template.transform({"user": {"name": "Alice", "age": 30}})
# -> {'name': 'Alice', 'year': 31}
```

## Installation

```bash
pip install -e "packages/jslt[dev]"   # depuis le dépôt ; installe aussi pytest + ruff
```

La seule dépendance d'exécution est `antlr4-python3-runtime`. Le parser généré
est **versionné** : aucun outil ANTLR (ni Java) n'est requis pour *utiliser* la
librairie — seulement pour *régénérer* le parser après modification des
grammaires.

## En un coup d'œil

| Capacité | Exemple de template | Source | Résultat |
|---|---|---|---|
| Constantes / structure | `{ "v": "Paris" }` | `{}` | `{"v": "Paris"}` |
| JSONPath | `{ "n": $.user.name }` | `{"user":{"name":"A"}}` | `{"n": "A"}` |
| Descente récursive | `{ "ids": $..id }` | `{"a":{"id":1},"b":{"id":2}}` | `{"ids":[1,2]}` |
| Variables | `{ "u:": $.user, "n": u:$.name }` | `{"user":{"name":"B"}}` | `{"n":"B"}` |
| Opérateurs | `{ "s": $.a + $.b }` | `{"a":1,"b":2}` | `{"s":3}` |
| Coalescence | `{ "v": $.x ?? "def" }` | `{}` | `{"v":"def"}` |
| Fonctions | `{ "t": sum($.n) }` | `{"n":[1,2,3]}` | `{"t":6}` |
| Casts | `{ "i": $.s #integer }` | `{"s":"42"}` | `{"i":42}` |
| `when` / `switch` | `{ "r": when($.x) { "a": 1, "default": 0 } }` | `{"x":"a"}` | `{"r":1}` |
| Boucles | `[ { "$source": $.u, "n": $.name } ]` | `{"u":[{"name":"A"}]}` | `[{"n":"A"}]` |
| Filtres JSONPath | `{ "g": $.items[?(@.n > 1)] }` | `{"items":[{"n":1},{"n":2}]}` | `{"g":[{"n":2}]}` |

Le **[guide complet avec de nombreux exemples testables](docs/guide.md)** détaille
chaque construction. Tous ses exemples sont exécutés par la suite de tests
(`tests/test_guide_examples.py`), ils ne peuvent donc pas « pourrir ».

## API publique

```python
from jslt import JsltTemplate

tpl = JsltTemplate.parse(source_str)   # compile le template (lève JsltSyntaxError si invalide)
tpl.transform(document)                # applique le template à un document (dict/list/scalaire)
tpl.to_source()                        # re-sérialise l'AST en template ré-analysable (ToString)
tpl.ast                                # l'AST (arbre de nœuds JsltBase)
```

Exceptions : `JsltError` (base), `JsltSyntaxError` (parsing), `JsltSemanticError`.
Les constructions reconnues par la grammaire mais non encore portées lèvent
`NotImplementedError` avec un message explicite (jamais un résultat faux).

## Extensibilité (fonctions & plugins)

Ajouter une fonction utilisable dans les templates, isoler un jeu de fonctions,
introspecter le registre, ou consommer des plugins tiers — équivalent idiomatique
Python du mécanisme de services du .NET :

```python
from jslt import jslt_function, JsltTemplate, default_registry

@jslt_function("double", description="Double un nombre")
def _double(ctx, x=None):
    return x * 2

JsltTemplate.parse('{ "r": double($.n) }').transform({"n": 21})   # -> {'r': 42}
default_registry.names()          # découverte : liste des fonctions disponibles
default_registry.describe("double").signature()   # 'double(x)'
```

Les **plugins tiers** sont auto-découverts via le groupe d'entry points
`jslt.functions` (installer le paquet suffit). Détails et contrat de plugin dans le
[guide, §Extensibilité](docs/guide.md#16-extensibilité--fonctions-et-plugins).

**Plugins officiels** (monorepo, distributions séparées) :
- [`jslt-csv`](packages/jslt-csv/) — lecture de fichiers CSV (`loadcsv`).
- [`jslt-xml`](packages/jslt-xml/) — lecture de fichiers XML (`loadxml`).
- [`jslt-db`](packages/jslt-db/) — lecture en base SQL (`connectsql`, `readsql`).
- [`jslt-http`](packages/jslt-http/) — appels HTTP (`http`, `httpget`).
- [`jslt-elastic`](packages/jslt-elastic/) — recherche Elasticsearch (`esconnect`, `essearch`).

## Architecture

Le pipeline suit celui du moteur .NET, **sans** son étage de génération /
compilation de code (Roslyn) : en Python, la transformation est réalisée par un
**interpréteur d'AST** (tree-walking), plus simple et portable, à comportement
identique. Le cœur est le paquet `packages/jslt/` (chemins ci-dessous relatifs à
ce dossier) ; les plugins d'E-S sont les autres `packages/jslt-*/`.

```
texte template
  └─ parser ANTLR (grammaire grammar/*.g4)      src/jslt/_antlr/ (généré, versionné)
       └─ arbre d'analyse ANTLR
            └─ ScriptBuilderVisitor               src/jslt/parsing/ (arbre ANTLR → AST)
                 └─ AST (pattern Visitor)         src/jslt/ast/
                      └─ interpréteur (tree-walk)  src/jslt/runtime/
                           ├─ JSONPath             src/jslt/jsonpath/ (port de Bb.JPaths, RFC 9535)
                           └─ fonctions            src/jslt/functions/ (registre par nom)
```

Patterns repris du .NET, notamment le **Visitor à double dispatch** (chaque nœud
`JsltBase` a `accept(visitor)` qui appelle `visitor.visit_xxx(self)`, mappé 1:1
aux noms .NET) et les **deux couches de visiteurs** (construction d'AST, puis
évaluation et sérialisation). Détails et écarts volontaires dans
[`CLAUDE.md`](CLAUDE.md).

## Développement

```bash
pip install -e "packages/jslt[dev]"
pytest packages/jslt/tests        # suite de tests du cœur
ruff check packages               # lint (le code généré _antlr/ est exclu)
bash packages/jslt/scripts/generate_parser.sh   # régénère le parser (Java requis)
```

La grammaire fait foi : `packages/jslt/grammar/JsltLexer.g4` et `JsltParser.g4`
sont la source de vérité du langage, reprise du dépôt .NET.

## Périmètre

Le portage cible le **cœur** du moteur. Hors périmètre (extensible) : certains
opérateurs ensemblistes de filtre (`nin`/`subsetof`/`contains`…, absents aussi du
.NET), les fonctions d'E-S (`csv`, `http`, `sql`…) et les jointures (`group`,
`join`, `index`). Le détail des fonctions portées et des écarts assumés vis-à-vis
du .NET figure dans [`CLAUDE.md`](CLAUDE.md).

## Licence

Apache-2.0 (comme le projet .NET d'origine).
