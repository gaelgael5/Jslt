# CLAUDE.md — urban-json (portage Python)

Portage Python du langage **JSLT** (JSON Stylesheet Language Transformations),
initialement en .NET : [Black-Beard-Sdk/jslt](https://github.com/Black-Beard-Sdk/jslt).
Le code .NET de référence est cloné (hors versionnement) sous `.net/` quand il
est présent.

## Principe directeur

Reproduire **fidèlement les patterns** du moteur .NET tout en restant
idiomatique Python. Fidèle au **comportement et aux tests** du .NET, **pas à ses
bugs** (voir « Écarts volontaires »).

## Architecture (miroir du .NET)

Le **cœur** vit sous `packages/urban-json/` (paquet `urban_json`), au même niveau que les
plugins. Chemins ci-dessous relatifs à `packages/urban-json/` :

```
texte template
  └─ parser ANTLR (grammaire grammar/*.g4)      src/urban_json/_antlr/ (généré, versionné)
       └─ arbre d'analyse ANTLR
            └─ ScriptBuilderVisitor               src/urban_json/parsing/ (arbre ANTLR -> AST)
                 └─ AST (pattern Visitor)         src/urban_json/ast/
                      └─ interpréteur (tree-walk)  src/urban_json/runtime/
                           ├─ JSONPath             src/urban_json/jsonpath/ (port de Bb.JPaths)
                           └─ fonctions            src/urban_json/functions/ (registre par nom)
```

Patterns repris du .NET :
- **Visitor à double dispatch** : chaque nœud `JsltBase` a `accept(visitor)` qui
  appelle `visitor.visit_xxx(self)`. Méthodes mappées 1:1 aux noms .NET
  (`VisitObject` → `visit_object`), documentées dans `ast/visitor.py`.
- **Deux couches de visiteurs** : `ScriptBuilderVisitor` (hérite du visiteur
  ANTLR généré, construit l'AST) puis les visiteurs sur l'AST (évaluation…).
- **Interpréteur d'AST** au lieu de la génération/compilation de code (Roslyn)
  du .NET — plus simple et portable, même comportement. Un **chemin compilé
  optionnel** (`src/urban_json/runtime/compiler.py`) accélère les transformations
  en masse sans changer l'API : `JsltTemplate.build()` parcourt l'AST une fois et
  produit, par nœud, une closure `program(context) -> valeur` (plus de
  double-dispatch ni de tests de type par nœud ; accès de champ `$.x` singulier
  compilé en descente `dict`/`list` directe ; opérateur binaire pré-résolu). Après
  `build()`, `transform` emprunte ce chemin, **résultat identique** à
  l'interpréteur (vérifié par `tests/test_compiler.py` sur tous les exemples du
  guide) ; sans `build()`, l'interpréteur reste le défaut. Tout nœud non compilé
  retombe sur l'interpréteur (closure de repli), donc jamais faux. Gain observé
  ×3 à ×5 (banc `benchmarks/bench_transform.py`).

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
- Regex (`regexismatch`/`regexmatches`) : dialecte du module `re` ; seuls les groupes
  nommés .NET `(?<nom>…)` sont traduits en `(?P<nom>…)`. `null`/objet/tableau → `null`
  (le .NET levait sur null) ; motif invalide → `JsltError`.
- `contains` est aussi un mot-clé (opérateur de filtre JSONPath) : la grammaire
  l'accepte désormais comme nom de fonction (`jsonfunctionName`), sinon la fonction
  `contains(...)` était inappelable — déjà le cas en .NET.
- Arguments « chemin » (`distinct`, `select`, `selectmany`, `selectany`) : compilés
  (`$.x`) **ou** en chaîne (`"$.x"`, forme .NET re-parsée à l'exécution).
- Argument en trop → `JsltError` lisible (le .NET résolvait par types ; Python
  levait une `TypeError` brute).
- `parsedate` : pas de type date dans le portage → chaîne ISO 8601 ; cultures
  « mois d'abord » = vide/invariant/en/en-US, toutes les autres « jour d'abord ».
- `format` : masques .NET **traduits** (sous-ensemble courant nombres/dates, 7
  cultures) dans `functions/formatting.py` ; hors sous-ensemble → `JsltError`. Une
  chaîne ISO est formatée comme une date (Newtonsoft convertit les ISO en dates).
- `group` multi-chemins : sous-groupes imbriqués (le .NET les perdait) ; `join` ne
  modifie pas la source (le .NET mutait la gauche) ; `createindex` rend un objet
  `{clé: élément}` (le .NET : `JDictionaryValue` opaque).
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
  déclarant le groupe d'entry points **`urban_json.functions`** (vrai équivalent du
  `AddAssembly` .NET). Auto-appelé une fois au 1er `transform` sur le registre
  global. Contrat : l'entry point pointe une callable `register(registry)`.
  Déclaration côté plugin :
  ```toml
  [project.entry-points."urban_json.functions"]
  mon_paquet = "mon_paquet.jslt_ext:register"
  ```
  API publique exportée au top-level `urban_json` : `jslt_function`, `FunctionRegistry`,
  `FunctionInfo`, `default_registry`, `load_plugins`.

C'est le mécanisme sur lequel s'appuient les **paquets additionnels** (E-S), hors
cœur, chacun comme **distribution séparée** dans un **monorepo** :

- `packages/urban-json-csv/` — fonctions `loadcsv` (port de `ServiceCsv`) et `loadmcsv`
  (CSV multi-enregistrements hiérarchique, port de `ServicesMultiCsv` + `Bb.MultiCsv` ;
  module `urban_json_csv.mcsv`). Distribution `urban-json-csv`, dépend de `urban-json`.
- `packages/urban-json-xml/` — fonction `loadxml` (conventions XML↔JSON Newtonsoft du
  `XmlNodeConverter` .NET ; parsing sécurisé via `defusedxml`). Distribution
  `urban-json-xml`, dépend de `urban-json` + `defusedxml`.
- `packages/urban-json-db/` — fonctions `connectsql` / `readsql` (port de `ServicesSql`).
  Distribution `urban-json-db` ; SQLite via la stdlib (sans dépendance), autres SGBD via
  un registre de clients DB-API (extras `postgresql`/`mysql`).
- `packages/urban-json-http/` — fonctions `http` / `httpget`. Appel formalisé en objet
  Fetch/`RequestInit` (`{method,url,headers,query,body}` → `{status,headers,body}`)
  via `httpx`. Distribution `urban-json-http`, dépend de `urban-json` + `httpx`.
- `packages/urban-json-elastic/` — fonctions `esconnect` / `essearch` (recherche
  Elasticsearch → `_source` des hits) via le client officiel `elasticsearch`
  (importé paresseusement). Distribution `urban-json-elastic`, dépend de `urban-json` +
  `elasticsearch`.
- `packages/urban-json-editor/` — composant d'édition **réutilisable** : Web Component
  `<jslt-editor>` (coloration syntaxique + intellisense, **sans dépendance JS**) +
  utilitaires Python (`assets_dir`, `catalog`, `mount`). L'intellisense est
  alimentée par `registry.catalog()`. Distribution `urban-json-editor`, dépend de `urban-json`.

### Applications (non publiées) — `apps/`

Les **applications** du dépôt vivent sous `apps/` (distinct de `packages/`, réservé
aux libs publiables) :

- `apps/playground/` — playground web de test/démo (FastAPI) : template jslt
  (via `<jslt-editor>`) + JSON source → résultat du **vrai moteur** côté serveur.
  **Bac à sable** : seules les fonctions du cœur sont exécutées (registre isolé,
  copie du registre cœur sans plugins) — pas d'E-S (fichiers/réseau/SQL) depuis un
  template. Lancer : `uvicorn urban_json_playground.app:app --reload`.
  **Machine de test** : image `apps/playground/Dockerfile` (cœur + éditeur installés
  depuis les sources du dépôt), stack `docker-compose.yml` à la racine, port hôte
  `PLAYGROUND_PORT` (`.env`, défaut 8080), sonde `/healthz`. Livrer : push sur `dev`,
  puis sur la machine `./dev-deploy.sh` (se met à jour depuis `origin/dev`, journal
  dans `deploy-logs/`). Déclaration à l'annuaire du portail : code TOTP (outil MCP
  `totp_code`) dans `PORTAL_TOKEN`, puis `./dev-deploy.sh --exposer-seulement` (le code
  expire en 30 s, bien avant la fin d'un build) ; script `scripts/declarer-exposition.sh`
  copié du dépôt du portail.

Modèle de packaging (cf. pytest) : **monorepo, distributions indépendantes,
découverte par entry points**. Chaque paquet (cœur compris) a son
`packages/<nom>/pyproject.toml`, son `src/`, ses tests, sa release (tag dédié :
cœur `vX.Y.Z` → `release.yml` ; plugins `urban-json-csv-vX.Y.Z` →
`release-urban-json-csv.yml`, etc.). À la racine : docs projet (`README*`, `docs/`,
`CLAUDE.md`) et `.github/`.

```bash
pip install -e "packages/urban-json[dev]"   # cœur + outils
pip install -e packages/urban-json-csv      # plugins (dépendent du cœur)
pip install -e packages/urban-json-xml
pip install -e packages/urban-json-db
pip install -e packages/urban-json-http
pip install -e packages/urban-json-elastic
pytest packages/urban-json/tests && pytest packages/urban-json-*/tests
ruff check packages
```

## Hors périmètre « cœur » (extensible, non porté)

- Opérateurs ensemblistes de filtre `nin`/`subsetof`/`contains`/`size`/`empty`
  (non implémentés côté .NET non plus). Le filtre `in` **est** porté.
- Fonctions de chemin : `length()` et `value()` **sont** portées (dans les
  chemins et les filtres) ; `count`/`match`/`search` (et `size`, inexistant en
  .NET) lèvent `NotImplementedError`.
- Fonctions d'E-S (`csv`, `http`, `hash`, `randoms`, `group`, `sql`).

Sérialisation `ToString` (round-trip AST → source) : **portée** sous forme d'un
visiteur dédié `SourceWriterVisitor` (`packages/urban-json/src/urban_json/serialization.py`), exposée via
`JsltTemplate.to_source()`. Produit un template valide et ré-analysable,
équivalent en comportement (pas identique au caractère près) ; un cast `x #type`
se re-sérialise sous sa forme `convert(x, "type")`.

Débogage de template (`packages/urban-json/src/urban_json/runtime/debug.py`) : le .NET
affichait le **code généré** (Roslyn) pour stepper au débogueur — non pertinent ici
(interpréteur, pas de code généré). À la place, on déboge **au niveau du template**
en instrumentant l'évaluateur : `DebugEvaluationVisitor` enveloppe chaque `visit_*`
et notifie un `Tracer` ; `TraceCollector` en tire une **trace pas-à-pas** (une
`TraceStep` par nœud : type, localisation, source courante, valeur) et marque les
**points d'arrêt** (par fonction / « méthode du contexte », ou par ligne). Exposé
via `JsltTemplate.debug(...)` → `DebugResult` (exportés : `DebugResult`,
`TraceStep`). Le playground l'utilise pour un pas-à-pas visuel (`/api/debug`).

Fonctions portées (modules dans `packages/urban-json/src/urban_json/functions/`) :
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

Le cœur est sous `packages/urban-json/` (chemins ci-dessous relatifs à ce dossier) :

```bash
pip install -e "packages/urban-json[dev]"           # runtime ANTLR + pytest + ruff
pytest packages/urban-json/tests                    # tests du cœur
ruff check packages                           # lint (le code généré _antlr/ est exclu)
bash packages/urban-json/scripts/generate_parser.sh # régénère le parser (Java requis)
```

Le parser généré (`packages/urban-json/src/urban_json/_antlr/`) est **versionné** : la
librairie s'utilise sans l'outil ANTLR. La grammaire `packages/urban-json/grammar/*.g4`
fait foi.

### Packaging / publication

```bash
cd packages/urban-json && python -m build   # construit sdist + wheel dans dist/
python -m twine check dist/*           # valide les distributions (métadonnées, README)
```

- Version **single-source** : `urban_json.__version__`
  (`packages/urban-json/src/urban_json/__init__.py`), lue par `[tool.setuptools.dynamic]`.
  Pour publier une version, bumper `__version__`.
- Deux canaux de publication, tous deux en **Trusted Publishing** (OIDC, aucun
  token stocké) :
  - **Prod → PyPI** (`release.yml` pour le cœur, `release-urban-json-<plugin>.yml`
    pour chaque plugin) : pousser un tag — cœur `vX.Y.Z` (égal à `__version__`,
    vérifié par le workflow), plugin `urban-json-<plugin>-vX.Y.Z`. Build + tests,
    puis publication sur PyPI. Environnement GitHub par paquet (`pypi`,
    `urban-json-csv`, …).
  - **Dev → TestPyPI** (`release-testpypi.yml`) : chaque push sur `dev` touchant
    `packages/**` publie tous les paquets du cœur/plugins sur **TestPyPI**, en
    version `X.Y.Z.dev<run_number>` (PEP 440, unique par exécution — la source
    n'est pas modifiée en dépôt, seulement en CI). Environnement `testpypi`.
    **Opt-in** : le job n'est actif que si la variable de dépôt
    `PUBLISH_TESTPYPI == 'true'` (sinon ignoré → CI verte), le temps de déclarer
    les éditeurs de confiance.
- Prérequis une fois, **par projet** et par index : créer le projet (sur PyPI
  et/ou TestPyPI) et déclarer l'éditeur de confiance GitHub
  (repo `gaelgael5/Jslt`, le `workflow` correspondant, l'`environment` ci-dessus).

## Conventions

- snake_case côté code maison ; les overrides du visiteur ANTLR restent en
  camelCase (API imposée par le générateur).
- Toute fonctionnalité portée s'accompagne de tests, dont, quand c'est possible,
  des cas repris de `Black.Beard.Jslt.UnitTests` comme oracle de conformité.
- Les constructions non encore portées lèvent `NotImplementedError` avec un
  message explicite plutôt que de produire un résultat faux.
