# Intégrer le moteur — guide jslt

*Français · [English](integration.en.md)*

[← Guide jslt](guide.md) · cette page documente les **points d'accroche** du
moteur pour une application qui l'embarque, et le niveau de garantie de chacun.

---

## Trois surfaces, trois garanties

| Surface | Import | Garantie |
|---|---|---|
| **API publique** | `from urban_json import …` (tout ce qui est dans `__all__`) | **stable**. Une rupture passe par une version mineure ou majeure, annoncée dans le [CHANGELOG](../CHANGELOG.md). |
| **Interne documentée** | `urban_json.parsing`, `urban_json.runtime`, `urban_json.ast`, `urban_json.jsonpath` | **documentée, non figée**. Ces noms existent et font ce qui est écrit ici ; un déplacement ou un changement de signature est **annoncé dans le CHANGELOG**, sans attendre une version majeure. |
| **Interne non documentée** | tout le reste : modules et fonctions préfixés `_`, `urban_json._antlr` (généré), les helpers de `functions/` | **aucune garantie**, peut changer dans n'importe quelle version. |

**Pourquoi cette page existe.** Une intégration s'appuyait sur `parse_to_tree`,
`ScriptBuilderVisitor`, `JsltEvaluationVisitor`, `RuntimeContext`, `Sources`,
`JsltKind` et les sélecteurs JSONPath — sans qu'aucune documentation ne dise si
ces noms étaient stables. Faute de contrat, la montée de version a dû être
validée en **comparant les sources de deux versions octet par octet** pour
constater que `parsing/`, `ast/`, `runtime/` et `jsonpath/` n'avaient pas bougé.
C'est le coût d'une surface non documentée : le travail de garantie retombe sur
l'intégrateur, à chaque version. La ligne du milieu existe pour cela, et le
CHANGELOG la sert.

## Le chemin courant

```python
from urban_json import JsltTemplate

template = JsltTemplate.parse(texte_du_template)       # -> AST, lève JsltSyntaxError
resultat = template.transform(document)                 # -> structures Python
texte = template.render(document)                       # -> texte ($directives.output)
```

- `transform(source, functions=…, parameters=…)` : `functions` isole le jeu de
  fonctions disponibles, `parameters` passe des réglages lus par `param("nom")`.
- `build()` active le chemin compilé (×3 à ×5 en masse) ; le résultat est
  **identique** à l'interpréteur, c'est vérifié sur tous les exemples du guide.
- `debug(...)` rend une trace pas-à-pas, `to_source()` re-sérialise l'AST.

## Le pipeline, pièce par pièce

```
texte  ──parse_to_tree──▶  arbre ANTLR  ──ScriptBuilderVisitor──▶  AST
                                                                    │
                                              JsltEvaluationVisitor │ (+ RuntimeContext)
                                                                    ▼
                                                                 résultat
```

| Pièce | Import | Rôle |
|---|---|---|
| `parse_to_tree(texte)` | `urban_json.parsing` | arbre d'analyse ANTLR (règle `script`) ; lève `JsltSyntaxError` avec `line` / `column` |
| `ScriptBuilderVisitor` | `urban_json.parsing` | arbre ANTLR → AST jslt (`.visit(tree)`) |
| `JsltBase`, `JsltKind` | `urban_json.ast` | nœuds de l'AST et leur nature (`JsltKind` est 1:1 avec l'enum .NET) |
| `JsltJsonVisitor`, `JsltBaseVisitor` | `urban_json.ast` | visiteur à double dispatch ; `JsltBaseVisitor` descend par défaut, on surcharge le `visit_*` qui intéresse |
| `Sources`, `RuntimeContext` | `urban_json.runtime` | documents source / état d'exécution (pile de source courante, variables, `parameters`, `token_result`) |
| `JsltEvaluationVisitor` | `urban_json.runtime` | interpréteur d'AST (`ast.accept(visitor)`) |
| `Program`, `compile_program` | `urban_json.runtime` | chemin compilé (closures) derrière `build()` |
| `JsonPath`, `PathScope`, `Node` | `urban_json.jsonpath` | chemin compilé : `evaluate(racine)` rend des `Node`, `select_values(racine)` les valeurs |
| `ISelector` et ses classes | `urban_json.jsonpath` | un sélecteur par construction (`NameSelector`, `IndexSelector`, `SliceSelector`, `WildcardSelector`, `FilterSelector`, `PathFunctionSelector`) |

Le pipeline complet, à la main — utile pour inspecter l'arbre entre deux
étapes, ou pour fournir un contexte préparé :

```python
from urban_json.parsing import ScriptBuilderVisitor, parse_to_tree
from urban_json.runtime import JsltEvaluationVisitor, RuntimeContext, Sources

ast = ScriptBuilderVisitor().visit(parse_to_tree('{ "a": $.x + 1, "lot": param("lot") }'))
contexte = RuntimeContext(Sources({"x": 2}), None, {"lot": "A-12"})
ast.accept(JsltEvaluationVisitor(contexte))      # {'a': 3, 'lot': 'A-12'}
```

`RuntimeContext(sources, functions, parameters)` : `functions` à `None` prend le
registre global. Les trois arguments sont positionnels et optionnels.

## Outiller un template sans l'exécuter

L'AST se parcourt avec un visiteur. Pour inventorier les fonctions qu'un
template appelle — audit, aide d'éditeur, statistiques :

```python
from urban_json import JsltTemplate
from urban_json.ast import JsltBaseVisitor, JsltFunctionCall

class NomsDeFonctions(JsltBaseVisitor):
    def __init__(self):
        self.noms = set()

    def visit_function(self, node: JsltFunctionCall):
        self.noms.add(node.name)
        return super().visit_function(node)   # continue la descente

visiteur = NomsDeFonctions()
JsltTemplate.parse('{ "a": upper($.x), "b": sort($.l, foldtext($)) }').ast.accept(visiteur)
sorted(visiteur.noms)      # ['foldtext', 'sort', 'upper']
```

**Pour autoriser ou refuser des fonctions, ne vous arrêtez pas là.** Un
inventaire d'AST répond « quelles fonctions ce texte nomme » ; il ne garantit pas
« quelles fonctions l'exécution pourra atteindre ». La garde fiable est un
**registre dédié**, parce que c'est lui que le moteur consulte à l'exécution :

```python
from urban_json import JsltTemplate, default_registry

sandbox = default_registry.copy()          # copie indépendante du registre global
for nom in ("http", "readsql", "loadjson"):
    sandbox.remove(nom)                    # rend False si la fonction n'y était pas
JsltTemplate.parse(texte).transform(document, functions=sandbox)
```

C'est ce que fait le playground du dépôt : registre isolé, fonctions du cœur
seulement, aucune E-S depuis un template. Un inventaire d'AST sert à **expliquer**
un refus ; le registre sert à le **tenir**.

Pour une aide d'éditeur, `registre.catalog()` rend une liste sérialisable JSON
(nom, description, paramètres typés, retour, signature, `path_args`,
`lazy_args`), et `describe(nom)` un `FunctionInfo`.

## Ce qui n'est pas une API

- `urban_json._antlr/` : code **généré** par ANTLR, versionné pour que la
  librairie s'utilise sans l'outil. La grammaire (`grammar/*.g4`) fait foi.
- `functions/_helpers.py`, `functions/_dateread.py`, `functions/_datecalc.py`,
  `functions/_schemacheck.py` : helpers internes, nommés `_` pour cela.
- Les internes de `functions/formatting.py` (tables de culture, jetons de
  masque) : réutilisés **à l'intérieur** du paquet par la lecture de dates et de
  nombres, pas destinés à l'extérieur.

Pour ajouter des fonctions, le point d'extension est documenté :
[Extensibilité](extensibilite.md) (décorateur `@jslt_function`, registre,
plugins par entry points).

---

**Voir aussi** : [CHANGELOG](../CHANGELOG.md) pour ce qui a bougé entre deux
versions, [`CLAUDE.md`](../CLAUDE.md) pour l'architecture et les écarts
volontaires vis-à-vis du .NET.

---

[← Guide jslt](guide.md)
