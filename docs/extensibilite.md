# Extensibilité, débogage et re-sérialisation — guide jslt

*Français · [English](extensibilite.en.md)*

[← Guide jslt](guide.md) · les exemples de cette page sont **exécutés par la
suite de tests** (`tests/test_guide_examples.py`), sous la forme de triplets
*template → entrée → sortie*.

---

## Extensibilité : fonctions et plugins

On peut **ajouter** ses propres fonctions, les **isoler**, les **découvrir**, et
consommer des **plugins tiers** installés — l'équivalent idiomatique Python du
mécanisme d'extension du moteur.

### Ajouter une fonction

```python
from urban_json import jslt_function, JsltTemplate

@jslt_function("double", description="Double un nombre")
def _double(ctx, x=None):
    return x * 2

JsltTemplate.parse('{ "r": double($.n) }').transform({"n": 21})   # -> {'r': 42}
```

Une fonction reçoit toujours le contexte d'exécution en premier paramètre (`ctx`),
puis les arguments du template. `path_args=(indices)` marque les arguments reçus
comme chemin JSONPath compilé (non évalué), comme pour `distinct`.

### Isoler un jeu de fonctions

Un registre dédié permet de limiter/isoler les fonctions disponibles (sandbox) :

```python
from urban_json import FunctionRegistry, default_registry, JsltTemplate

sandbox = FunctionRegistry()                      # vide : aucune fonction intégrée
sandbox.register("triple", lambda ctx, x=None: x * 3)
JsltTemplate.parse('{ "r": triple($.n) }').transform({"n": 7}, functions=sandbox)

# Partir des fonctions intégrées sans muter le registre global :
derive = default_registry.copy()
derive.register("triple", lambda ctx, x=None: x * 3)
```

### Découvrir les fonctions disponibles

```python
from urban_json import default_registry

default_registry.names()                 # ['abs', 'concat', 'distinct', ...]
info = default_registry.describe("distinct")
info.signature()                         # 'distinct(source, path)'
info.path_args                           # (1,)
info.description                         # 1re ligne du docstring
info.parameters[1].name, info.parameters[1].type, info.parameters[1].is_path
#                                        # ('path', 'Any', True)
```

Pour alimenter un **éditeur de templates** (auto-complétion, aide contextuelle),
`catalog()` renvoie une liste **sérialisable JSON** décrivant chaque fonction
(nom, description, paramètres nom + type + requis + chemin, type de retour,
signature) :

```python
import json
from urban_json import default_registry

json.dumps(default_registry.catalog())   # prêt à transmettre à un éditeur
# [{"name": "distinct", "description": "...", "signature": "distinct(source, path)",
#   "parameters": [{"name": "source", "type": "Any", "required": false, ...},
#                  {"name": "path", "type": "Any", "is_path": true, ...}],
#   "returns": "list", "path_args": [1]}, ...]
```

### Plugins tiers (entry points)

Un paquet installé expose ses fonctions en déclarant le groupe d'entry points
`urban_json.functions`. Côté plugin, dans son `pyproject.toml` :

```toml
[project.entry-points."urban_json.functions"]
mon_paquet = "mon_paquet.jslt_ext:register"
```

avec une fonction `register` qui enregistre dans le registre reçu :

```python
def register(registry):
    registry.register("shout", lambda ctx, s=None: (s or "").upper() + "!")
```

Les plugins sont découverts **automatiquement** au premier `transform` (ou à la
demande via `load_plugins()`), puis utilisables dans les templates comme les
fonctions intégrées. C'est le mécanisme prévu pour les paquets additionnels (E-S :
CSV, bases de données, Elasticsearch…).

---

## Débogage (pas à pas)

`JsltTemplate.debug(source)` évalue le template en collectant une **trace
pas-à-pas** : une étape par nœud évalué, avec sa localisation, la source courante et
la valeur produite. (Le moteur étant un interpréteur, le débogage se fait au niveau
du template : le moteur interprète l'AST, il n'engendre pas de code.)

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

**Points d'arrêt** : marquer les étapes correspondant à une fonction (« méthode du
contexte ») ou à une ligne du template.

```python
r = JsltTemplate.parse('{ "t": sum($.n) }').debug({"n": [1, 2]}, break_functions=["sum"])
[s.expression for s in r.steps if s.breakpoint]   # ['sum(…)']
```

`DebugResult` porte `result` (valeur finale), `steps` (liste de `TraceStep`) et
`error` (message si l'évaluation échoue — la trace partielle reste disponible). Le
playground (`apps/playground`) en offre un pas-à-pas visuel.

---

## Re-sérialisation `to_source()`

`JsltTemplate.to_source()` reconstruit un template **valide et ré-analysable** à
partir de l'AST. Le résultat est équivalent en
**comportement** (pas forcément identique au caractère près) ; un cast `#type` y
réapparaît sous sa forme `convert(x, "type")`.

```python
from urban_json import JsltTemplate

tpl = JsltTemplate.parse('{ "sum": $.a + $.b }')
tpl.to_source()                          # -> '{ "sum": $.a + $.b }'
JsltTemplate.parse(tpl.to_source())      # ré-analysable sans erreur
```


---

[← Guide jslt](guide.md)
