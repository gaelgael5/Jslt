# jslt (Python)

Portage Python du langage **JSLT — JSON Stylesheet Language Transformations** :
un langage de **transformation JSON → JSON piloté par template**, initialement
implémenté en .NET ([Black-Beard-Sdk/jslt](https://github.com/Black-Beard-Sdk/jslt)).

Un template décrit la structure du JSON cible, avec des opérateurs : chemins
JSONPath (`$.x`), variables (`var:`), fonctions (`sum(...)`), boucles
(`[ { "$source": $.items } ]`), conditions (`when`), casts (`#integer`), etc.

```python
from jslt import JsltTemplate

template = JsltTemplate.parse('{ "name": $.n }')
result = template.transform({"n": "Alice"})   # (disponible à partir de la Phase 1)
# -> {"name": "Alice"}
```

## État du portage

Le portage se concentre sur le **cœur** du moteur (parser + AST + évaluation +
JSONPath + fonctions intégrées). L'outillage périphérique du dépôt .NET
(interface WPF, éditeur, stockage SQL…) n'est pas porté.

| Phase | Contenu | État |
|-------|---------|------|
| 0 | Analyse syntaxique (parser ANTLR) | ✅ |
| 1 | AST + transformation « défaut » | à venir |
| 2 | Variables + JSONPath simple | à venir |
| 3 | Boucles, opérateurs, casts | à venir |
| 4 | Fonctions intégrées + `when`/switch | à venir |
| 5 | JSONPath avancé (filtres, slices, descente) | à venir |

## Architecture

Le pipeline suit celui du moteur .NET, sans son étage de génération/compilation
de code (Roslyn) : en Python, la transformation est réalisée par un
**interpréteur d'AST** (tree-walking), plus simple et portable.

```
texte template
   └─ parser ANTLR (grammaire .g4)      src/jslt/_antlr/ (généré)
        └─ arbre d'analyse ANTLR
             └─ construction de l'AST    src/jslt/ast, src/jslt/parsing
                  └─ interpréteur        src/jslt/runtime
                       ├─ JSONPath       src/jslt/jsonpath
                       └─ fonctions      src/jslt/functions
```

## Développement

```bash
# Installer la librairie + dépendances de dev (runtime ANTLR, pytest, ruff)
pip install -e ".[dev]"

# Lancer les tests
pytest

# Régénérer le parser après modification des grammaires (grammar/*.g4)
#   nécessite Java ; télécharge l'outil ANTLR dans tools/ si absent
bash scripts/generate_parser.sh
```

La grammaire fait foi : les fichiers `grammar/JsltLexer.g4` et
`grammar/JsltParser.g4` sont la source de vérité du langage, repris du dépôt
.NET. Le parser Python généré (`src/jslt/_antlr/`) est versionné afin que la
librairie s'utilise sans l'outil ANTLR.

## Licence

Apache-2.0 (comme le projet .NET d'origine).
