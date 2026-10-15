# jslt

Portage Python du langage **JSLT — JSON Stylesheet Language Transformations** :
un langage de **transformation JSON → JSON piloté par template**, initialement
implémenté en .NET ([Black-Beard-Sdk/jslt](https://github.com/Black-Beard-Sdk/jslt)).

C'est le **paquet cœur** (moteur : parser, AST, interpréteur, JSONPath, fonctions
intégrées, extensibilité). Les capacités d'E-S (CSV, XML, SQL, HTTP, Elasticsearch)
sont des **plugins séparés** (`jslt-csv`, `jslt-xml`, `jslt-db`, `jslt-http`,
`jslt-elastic`) découverts automatiquement.

```python
from jslt import JsltTemplate

template = JsltTemplate.parse('{ "name": $.user.name, "year": $.user.age + 1 }')
template.transform({"user": {"name": "Alice", "age": 30}})
# -> {'name': 'Alice', 'year': 31}
```

## Installation

```bash
pip install jslt
```

Unique dépendance d'exécution : `antlr4-python3-runtime`. Le parser généré est
embarqué (aucun outil ANTLR ni Java requis pour *utiliser* la librairie).

## Documentation

- **Guide complet avec exemples testables** :
  <https://github.com/gaelgael5/Jslt/blob/main/docs/guide.md>
  ([English](https://github.com/gaelgael5/Jslt/blob/main/docs/guide.en.md))
- **Vue d'ensemble du projet et des plugins** :
  <https://github.com/gaelgael5/Jslt>

## API

```python
from jslt import JsltTemplate

tpl = JsltTemplate.parse(source_str)   # compile (JsltSyntaxError si invalide)
tpl.transform(document)                # applique le template à un document
tpl.to_source()                        # re-sérialise l'AST (ToString)
```

Extensibilité (ajouter/isoler/découvrir des fonctions, plugins via entry points
`jslt.functions`) : voir le guide, section Extensibilité.

## Licence

Apache-2.0 (comme le projet .NET d'origine).
