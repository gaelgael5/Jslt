# urban-json

*Français · [English](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json/README.en.md)*

Portage Python du langage **JSLT — JSON Stylesheet Language Transformations** :
un langage de **transformation JSON → JSON piloté par template**, initialement
implémenté en .NET ([Black-Beard-Sdk/jslt](https://github.com/Black-Beard-Sdk/jslt)).

C'est le **paquet cœur** (moteur : parser, AST, interpréteur, JSONPath, 75
fonctions intégrées, extensibilité). Les entrées-sorties et la génération
aléatoire sont des **plugins séparés**, découverts automatiquement une fois
installés : `urban-json-csv`, `urban-json-xml`, `urban-json-db`, `urban-json-http`,
`urban-json-elastic`, `urban-json-files`, `urban-json-html`, `urban-json-excel`,
`urban-json-phone`, `urban-json-random`. Le composant d'édition
`urban-json-editor` (Web Component `<jslt-editor>`) est également distribué à part.

```python
from urban_json import JsltTemplate

template = JsltTemplate.parse('{ "name": $.user.name, "year": $.user.age + 1 }')
template.transform({"user": {"name": "Alice", "age": 30}})
# -> {'name': 'Alice', 'year': 31}
```

## Installation

```bash
pip install urban-json
```

Unique dépendance d'exécution : `antlr4-python3-runtime`. Le parser généré est
embarqué (aucun outil ANTLR ni Java requis pour *utiliser* la librairie).

## Documentation

- **Guide complet avec exemples testables** (découpé par thème) :
  <https://github.com/gaelgael5/Jslt/blob/main/docs/guide.md>
  ([English](https://github.com/gaelgael5/Jslt/blob/main/docs/guide.en.md)) — notamment
  [chemins](https://github.com/gaelgael5/Jslt/blob/main/docs/chemins.md),
  [expressions](https://github.com/gaelgael5/Jslt/blob/main/docs/expressions.md),
  [collections](https://github.com/gaelgael5/Jslt/blob/main/docs/collections.md),
  [texte et formatage](https://github.com/gaelgael5/Jslt/blob/main/docs/texte.md),
  [dates et heures](https://github.com/gaelgael5/Jslt/blob/main/docs/dates.md),
  [objets](https://github.com/gaelgael5/Jslt/blob/main/docs/objets.md),
  [types et validation](https://github.com/gaelgael5/Jslt/blob/main/docs/types.md),
  [encodage et empreintes](https://github.com/gaelgael5/Jslt/blob/main/docs/encodage.md)
- **Intégrer le moteur** (API publique, internes documentés, bac à sable) :
  <https://github.com/gaelgael5/Jslt/blob/main/docs/integration.md>
- **Journal des modifications** : <https://github.com/gaelgael5/Jslt/blob/main/CHANGELOG.md>
- **Vue d'ensemble du projet et des plugins** :
  <https://github.com/gaelgael5/Jslt>

## API

```python
from urban_json import JsltTemplate

tpl = JsltTemplate.parse(source_str)   # compile (JsltSyntaxError si invalide)
tpl.transform(document)                # applique le template à un document
tpl.debug(document)                     # trace pas-à-pas (débogage)
tpl.to_source()                        # re-sérialise l'AST (ToString)
```

Extensibilité (ajouter/isoler/découvrir des fonctions, plugins via entry points
`urban_json.functions`) : voir le guide, section Extensibilité.

## Licence

Apache-2.0 (comme le projet .NET d'origine).
