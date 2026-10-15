# CLAUDE.md — jslt (portage Python)

Portage Python du langage **JSLT** (JSON Stylesheet Language Transformations),
initialement en .NET : [Black-Beard-Sdk/jslt](https://github.com/Black-Beard-Sdk/jslt).
Le code .NET de référence est cloné (hors versionnement) sous `.net/` quand il
est présent.

## Principe directeur

Reproduire **fidèlement les patterns** du moteur .NET tout en restant
idiomatique Python. Fidèle au **comportement et aux tests** du .NET, **pas à ses
bugs** (voir « Écarts volontaires »).

## Architecture (miroir du .NET)

```
texte template
  └─ parser ANTLR (grammaire grammar/*.g4)      src/jslt/_antlr/ (généré, versionné)
       └─ arbre d'analyse ANTLR
            └─ ScriptBuilderVisitor               src/jslt/parsing/ (arbre ANTLR -> AST)
                 └─ AST (pattern Visitor)         src/jslt/ast/
                      └─ interpréteur (tree-walk)  src/jslt/runtime/
                           ├─ JSONPath             src/jslt/jsonpath/ (port de Bb.JPaths)
                           └─ fonctions            src/jslt/functions/ (registre par nom)
```

Patterns repris du .NET :
- **Visitor à double dispatch** : chaque nœud `JsltBase` a `accept(visitor)` qui
  appelle `visitor.visit_xxx(self)`. Méthodes mappées 1:1 aux noms .NET
  (`VisitObject` → `visit_object`), documentées dans `ast/visitor.py`.
- **Deux couches de visiteurs** : `ScriptBuilderVisitor` (hérite du visiteur
  ANTLR généré, construit l'AST) puis les visiteurs sur l'AST (évaluation…).
- **Interpréteur d'AST** au lieu de la génération/compilation de code (Roslyn)
  du .NET — plus simple et portable, même comportement.

## Décisions de conception

- **Parser** : un seul, via la grammaire ANTLR. Le JSONPath est compilé une fois
  depuis l'arbre ANTLR (choix « B2 » ; le .NET re-parse la chaîne à l'exécution).
- **Moteur JSONPath** : port de `Bb.JPaths` (RFC 9535), pas de dépendance tierce.
- **Registre de fonctions** par **nom** (pas de résolution par types comme le
  .NET, inutile en Python dynamique). Un paramètre peut être marqué « chemin »
  via `path_args=(indices)` sur `@jslt_function` : il est alors reçu comme
  `JsonPath` compilé (non évalué), ce qui permet des fonctions comme `distinct`.
- **Scope de variables** : chaîne de résolveurs lexicale (port de
  `VariableResolver`/`VariableManager`).

## Écarts volontaires vs .NET (documentés)

- Règle `WS` réactivée dans la grammaire (le .NET tolérait les espaces via la
  récupération d'erreur ANTLR) — équivalent, mais parsing strict.
- Bug `VisitJsonValueInteger` (renvoyait 0) **non** reproduit.
- Précédence des opérateurs **standard** (le .NET regroupait par parité, non
  testé).
- `^` = XOR entier, `&`/`|` = ET/OU bit-à-bit, `&&` = ET booléen (fidèles) ;
  `||` = OU booléen (corrige un copier-coller fautif .NET qui faisait un ET).
- Casts temporels (`uri`/`uuid`/`datetime`/`time`) rendus en chaîne (simplifié) ;
  `integer`/`decimal`/`string`/`boolean` complets.

## Extensibilité (fonctions & plugins)

Équivalent Python du `ServiceContainer`/`ServiceDiscovery` .NET, rendu idiomatique
(pas de scan d'assembly par réflexion : inutile en Python) :

- **Ajouter** une fonction : décorateur `@jslt_function("nom", path_args=(), description="")`
  (analogue de l'attribut `[JsltExtensionMethod]`) ou `registry.register(...)`.
- **Isoler** : `transform(source, functions=mon_registre)` ; `FunctionRegistry()`
  vide ou `default_registry.copy()` pour dériver sans muter le global.
- **Découvrir** : `registry.names()`, `describe(nom) -> FunctionInfo`,
  `describe_all()`, itération, `in` (casse ignorée). `FunctionInfo` porte nom,
  paramètres typés (`ParameterInfo` : nom, type, requis/défaut, `is_path`,
  variadic), type de retour, `path_args`, description, `signature()`.
- **Pour un éditeur (intellisense)** : `registry.catalog()` renvoie une liste de
  dicts **sérialisables JSON** (nom, description, paramètres nom+type, retour,
  signature) — analogue du paquet `Intellisense` du .NET. Les types proviennent
  des annotations ; chaque fonction portée/plugin gagne à être annotée + docstring.
- **Plugins tiers** : `load_plugins(registry=default_registry)` découvre les paquets
  déclarant le groupe d'entry points **`jslt.functions`** (vrai équivalent du
  `AddAssembly` .NET). Auto-appelé une fois au 1er `transform` sur le registre
  global. Contrat : l'entry point pointe une callable `register(registry)`.
  Déclaration côté plugin :
  ```toml
  [project.entry-points."jslt.functions"]
  mon_paquet = "mon_paquet.jslt_ext:register"
  ```
  API publique exportée au top-level `jslt` : `jslt_function`, `FunctionRegistry`,
  `FunctionInfo`, `default_registry`, `load_plugins`.

C'est le mécanisme sur lequel s'appuient les **paquets additionnels** (E-S), hors
cœur, chacun comme **distribution séparée** dans un **monorepo** :

- `packages/jslt-csv/` — fonction `loadcsv` (port de `ServiceCsv`). Distribution
  `jslt-csv`, dépend de `jslt`.
- `packages/jslt-xml/` — fonction `loadxml` (conventions XML↔JSON Newtonsoft du
  `XmlNodeConverter` .NET ; parsing sécurisé via `defusedxml`). Distribution
  `jslt-xml`, dépend de `jslt` + `defusedxml`.
- À venir (même modèle) : bases de données, Elasticsearch, `http`, `loadmcsv`…

Modèle de packaging (cf. pytest) : **monorepo, distributions indépendantes,
découverte par entry points**. Le cœur reste à la racine ; chaque plugin a son
`packages/<nom>/pyproject.toml`, son `src/`, ses tests, sa release (tag dédié,
p.ex. `jslt-csv-vX.Y.Z` → `.github/workflows/release-jslt-csv.yml`).

```bash
pip install -e ".[dev]"            # cœur + outils
pip install -e packages/jslt-csv   # plugins (dépendent du cœur)
pip install -e packages/jslt-xml
pytest && pytest packages/jslt-csv/tests packages/jslt-xml/tests
ruff check src tests packages
```

## Hors périmètre « cœur » (extensible, non porté)

- Opérateurs ensemblistes de filtre `nin`/`subsetof`/`contains`/`size`/`empty`
  (non implémentés côté .NET non plus). Le filtre `in` **est** porté.
- Fonctions de chemin : `length()` et `value()` **sont** portées (dans les
  chemins et les filtres) ; `count`/`match`/`search` (et `size`, inexistant en
  .NET) lèvent `NotImplementedError`.
- Fonctions d'E-S (`csv`, `http`, `hash`, `randoms`, `group`, `sql`).

Sérialisation `ToString` (round-trip AST → source) : **portée** sous forme d'un
visiteur dédié `SourceWriterVisitor` (`src/jslt/serialization.py`), exposée via
`JsltTemplate.to_source()`. Produit un template valide et ré-analysable,
équivalent en comportement (pas identique au caractère près) ; un cast `x #type`
se re-sérialise sous sa forme `convert(x, "type")`.

Fonctions portées (modules dans `src/jslt/functions/`) :
- cœur : `sum`, `concat`, `convert` (casts), `distinct`.
- maths : `abs`, `floor`, `round`, `truncate`, `min`, `max`, `sqrt`, `pow`, `exp`,
  `logarithm`/`logarithm10`/`logarithm2`, trig (`sin`/`cos`/`tan`/`asin`/`acos`/
  `atan`/`sinh`/`cosh`/`tanh`/`asinh`/`acosh`/`atanh`/`atan2`), `pi`, `e`.
- texte : `upper`, `lower`, `trim`, `split`, `startswith`, `endswith`,
  `stringcontains`, `indexof`, `lastindexof`, `padleft`, `padright`, `stringlenght`.
- encodage : `tobase64`, `frombase64`, `crc32`, `sha256`, `sha512`.
- collections : `limit`, `union`, `select`, `selectmany` (`select`/`selectmany`
  prennent un argument-chemin).
- divers : `uuid`, `now`, `isnull`, `isnotnull`.

Quirks .NET conservés : `floor`/`round`/`truncate`/`min`/`max`/`pow`/trig
renvoient un flottant, `round` = arrondi bancaire, `min`/`max` sont binaires.
Fonctions encore non portées : `format`, `normalize`, `group`/`join`/`index`/
`createindex` (jointures), `getrandom_*`, E-S (`loadcsv`/`loadjson`/http).

## Développement

```bash
pip install -e ".[dev]"      # runtime ANTLR + pytest + ruff
pytest                       # tests
ruff check src tests         # lint (le code généré _antlr/ est exclu)
bash scripts/generate_parser.sh   # régénère le parser après modif des grammar/*.g4 (Java requis)
```

Le parser généré (`src/jslt/_antlr/`) est **versionné** : la librairie s'utilise
sans l'outil ANTLR. La grammaire `grammar/*.g4` fait foi.

### Packaging / publication

```bash
python -m build              # construit sdist + wheel dans dist/
python -m twine check dist/* # valide les distributions (métadonnées, README)
```

- Version **single-source** : `jslt.__version__` (`src/jslt/__init__.py`), lue par
  `[tool.setuptools.dynamic]`. Pour publier une version, bumper `__version__`.
- Publication **automatisée** (`.github/workflows/release.yml`) : pousser un tag
  `vX.Y.Z` (égal à `__version__`, vérifié par le workflow) build, teste, puis
  publie sur PyPI via **Trusted Publishing** (OIDC, aucun token stocké).
  Prérequis PyPI une fois : créer le projet + déclarer l'éditeur de confiance
  (repo `gaelgael5/Jslt`, workflow `release.yml`, environnement `pypi`).

## Conventions

- snake_case côté code maison ; les overrides du visiteur ANTLR restent en
  camelCase (API imposée par le générateur).
- Toute fonctionnalité portée s'accompagne de tests, dont, quand c'est possible,
  des cas repris de `Black.Beard.Jslt.UnitTests` comme oracle de conformité.
- Les constructions non encore portées lèvent `NotImplementedError` avec un
  message explicite plutôt que de produire un résultat faux.
