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
  **Étendu au-delà du .NET** (`functions/dates.py`) : 3e argument `masque` (lecture
  stricte selon le vocabulaire .NET de `format`, inversé dans `functions/_dateread.py`
  pour que lire et écrire partagent un seul vocabulaire ; largeurs strictes façon
  `ParseExact`) et 4e argument `fuseau` (nom IANA via `zoneinfo`, `UTC`/`Z`, ou
  décalage fixe ; il **qualifie** une date naïve et **convertit** une date qui porte
  déjà un décalage). Composante absente du masque → époque Unix, pas « aujourd'hui »
  comme le .NET : le résultat d'un template ne doit pas dépendre du jour d'exécution.
- **Calcul, écart et extraction de dates, sans contrepartie .NET** : `dateadd` /
  `datesub` (unités `second`→`year`, pluriel toléré, `n` entier), `datediff(début,
  fin, unité)` et `datepart` (`year`, `month`, `day`, `dayofweek`, `hour`, `minute`,
  `second`). `month`/`year` sont calendaires : `dateadd` **borne** le jour sur les
  mois courts (comme `AddMonths`), `datediff` ne compte un mois que si le jour et
  l'heure de `fin` ont rattrapé ceux de `début` — les deux ne sont donc pas
  exactement inverses, et c'est documenté dans le guide. `datediff` tronque **vers
  zéro** (pas vers -∞ comme `//`) et refuse de comparer une date avec fuseau à une
  date sans fuseau. `dayofweek` suit la convention `DayOfWeek` du .NET
  (dimanche = 0), pas ISO. `null` est propagé, mais une valeur qui n'est pas une
  date ISO lève — un `null` silencieux ferait découvrir le défaut de données très
  loin de sa cause.
- `format` : masques .NET **traduits** (sous-ensemble courant nombres/dates, 7
  cultures) dans `functions/formatting.py` ; hors sous-ensemble → `JsltError`. Une
  chaîne ISO est formatée comme une date (Newtonsoft convertit les ISO en dates),
  `Z` final compris (`fromisoformat` ne l'accepte qu'à partir de Python 3.11, on
  normalise). Les jetons de décalage `z`/`zz`/`zzz`/`K` sont **écrits** (ils
  levaient), pour que `parsedate(…, fuseau)` et `format` fassent l'aller-retour ;
  `z` sur une date sans décalage écrit zéro, là où le .NET prendrait celui de la
  machine — la sortie ne doit pas dépendre du serveur. Un spécificateur seul
  (`"z"`, `"K"`) reste refusé, comme en .NET (masque d'une lettre = masque standard).
- **Une seule mise en texte** : `to_text` rend le **JSON compact** d'un tableau
  ou d'un objet (comme `token.ToString()` côté Newtonsoft). Jusqu'en 0.6.0 elle
  rendait `str(valeur)`, donc du `repr` Python avec guillemets simples, qui
  ressortait dans le JSON produit (`concat` d'un tableau imbriqué, clef composite
  de `groupby`) alors que le cast `#string` passait déjà par le JSON. `stringify`
  reste comme nom explicite du contrat, sans comportement propre.
- **Refus et observation depuis le template** : `require` / `requirethat` lèvent
  une `JsltError` porteuse d'un message métier (donc rattrapable par
  `trydefault`) ; `trace` / `traces` écrivent dans `RuntimeContext.traces`, pas
  dans un état global — deux exécutions concurrentes ne se mélangent pas, et un
  intégrateur lit le journal après coup. `require` ne refuse que l'**absence**
  (`0`, `false`, `""` sont des valeurs) ; `requirethat` exige `true` **strict**,
  parce qu'une condition qui vaut `0` est presque toujours une expression qu'on
  croyait booléenne.
- **Écriture CSV / XML / YAML** (`_writers.py`, sans dépendance) : colonnes = union
  des clés rencontrées (se limiter au premier objet perdrait des données sur un
  flux hétérogène), valeurs imbriquées aplaties par `flattenobject`, conventions
  XML de `parsexml` (`@attribut`, `#text`, tableau = élément répété), YAML en
  sous-ensemble assumé (ni ancres, ni tags, ni littéral multi-ligne) qui **cite**
  tout scalaire relisible comme un autre type.
- **Un sens de tri par clef** : `sort($.l, [$.a, $.b], [true, false])` acceptait
  un booléen et un seul, donc le même sens pour toutes les clefs — un `reverse`
  inverse l'ordre complet. La forme en tableau compare **composante par
  composante** (`cmp_to_key`), ce qui coûte une comparaison Python par couple au
  lieu d'un tri sur clefs : seule cette forme le paie. Un sens manquant vaut
  croissant (comme l'argument omis), un sens **en trop lève** — c'est la faute
  d'écriture la plus probable et elle laisserait un tri d'apparence juste.
- **`groupby` imbriqué** (3e argument) : une clef composite rendait une clef
  **textuelle** (`["FR","Lyon"]`, en JSON compact depuis la correction de
  `to_text`) qu'il fallait re-analyser pour s'en servir ; imbriqué, le résultat
  se relit par chemin. Deux éléments dont les clefs n'ont pas la même longueur
  **lèvent** : la même clef porterait à la fois des éléments et un sous-groupe, et
  l'un des deux disparaîtrait. La forme plate reste le défaut (elle est
  réductible par `entries`).
- **`sumby` / `avgby`** : le total par groupe demandait quatre fonctions
  imbriquées (`fromentries` + `entries` + `groupby` + `sum(selectmany(…))`) pour
  l'usage le plus fréquent du regroupement. La valeur agrégée est un argument
  **paresseux**, omis il vaut l'élément (convention de `sort`/`distinctby`), et
  une valeur non numérique **lève** comme pour `sum`.
- **`unzip`** : réciproque de `zip`, qui n'en avait pas. Il s'arrête à la rangée
  la plus courte, pour la même raison que `zip` tronque au plus court ; mais une
  rangée qui n'est pas un tableau **lève**, écart assumé à la convention de la
  famille (non-tableau → `null`) : ici la source *est* un tableau, donc le chemin
  était bon, et un `null` global ferait chercher l'erreur au mauvais endroit.
- **Ordre total du tri** (`ordering.order_key`) : `null` < booléens < nombres <
  chaînes < tableaux < objets ; dans un rang, les nombres numériquement, les
  chaînes par points de code, les tableaux **élément par élément** et les objets
  par clés triées puis valeurs. Les tableaux étaient comparés par leur JSON
  compact jusqu'en 0.5.0 : un tri **multi-clefs** (`sort($.l, [$.a, $.b])`, usage
  naturel puisque la clef est une expression) ordonnait alors `[10]` avant `[2]`.
  Comparer récursivement coûte un peu plus et c'est le prix de la justesse.
- **Familles de fonctions ajoutées au-delà du .NET** (sujets 1 à 11 comblés en
  0.4.0, catégories collections / statistiques / texte / nombres en 0.5.0, cf.
  `CHANGELOG.md`). Décisions de 0.5.0 : `split` garde son 1er caractère (fidélité
  .NET) d'où `splitstring` ; `indexof` sur tableau compare la **structure** là où
  `contains` garde l'égalité `==` du langage ; `intersect`/`difference`
  dédupliquent et gardent l'ordre de gauche ; `variance`/`stddev` sont de
  **population** par défaut (les données d'un template sont l'ensemble, pas un
  tirage) ; `mode` accepte toutes les valeurs ; `groupby` rend un objet (donc
  réductible par `entries`) là où `group` garde la forme .NET ; `shorten` ne
  s'appelle pas `truncate` (déjà pris par la troncature numérique) et remonte au
  dernier espace ; `reverse` d'une chaîne travaille par **graphème** ;
  `log(x, 10)` passe par `log10` sinon il rendrait 2.9999999999999996. Décisions qui se lisent mal dans le code seul :
  `substring` **ne lève pas** sur des bornes trop larges (un template transforme
  des données qu'il ne choisit pas ; une longueur négative lève, elle) ;
  `regexreplace` suit la convention des regex (scalaire converti en texte) et non
  celle des chaînes (`false`) ; `sort` définit un **ordre total** (null <
  booléens < nombres < chaînes < tableaux < objets, chaînes par points de code)
  pour ne jamais lever sur des données mélangées, et sa clef s'évalue **par
  élément** — convention différente de `distinct`, dont le chemin s'applique au
  tableau entier ; les agrégats **lèvent** sur un élément non numérique comme
  `sum` ; `avg`/`median`/`min`/`max` d'un tableau vide valent `null` (0 serait une
  réponse fausse), `product` vaut 1 (élément neutre) ; `count` compte aussi les
  clés d'un objet et les caractères d'un texte, et vaut 1 pour un scalaire ;
  `has` existe parce qu'`isnull` ne distingue pas clé absente et valeur nulle ;
  `merge` est **plat** par défaut et ne mute pas ses sources ; `renamekeys` laisse
  le dernier écrit gagner une collision (lever casserait une migration en cours) ;
  la validation de schéma **ignore** les mots-clés non gérés (lever la rendrait
  inutilisable sur les schémas réels — validation utile, pas complète) ;
  `weekday` ne connaît **aucun** calendrier de jours fériés (il dépend du pays et
  de l'année) ; `datestartof(…, "week")` commence **lundi** (ISO) alors que
  `datepart(…, "dayofweek")` suit le .NET (dimanche = 0) — les deux choix sont
  délibérés ; `md5`/`sha1` sont là pour l'**identité**, jamais la signature, d'où
  `hmacsha256` (concaténer secret + message avant un `sha256` expose à
  l'extension de longueur) ; `tohex` écrit le signe devant les chiffres (un entier
  JSON n'a pas de largeur, donc pas de complément à deux) ; `parsejson`,
  `parsenumber` et `parsexml`/`parsecsv` **lèvent** sur une entrée illisible.
- **Arguments paresseux** (`lazy_args` sur `@jslt_function`) : une position peut
  être reçue **non évaluée**, sous forme de callable, que la fonction appelle
  quand elle veut et contre la source qu'elle empile. C'est ce qui permet la clef
  de tri par élément (`sort`) et le repli non évalué (`trydefault`). Le
  mécanisme est posé aux **deux** points d'appel (interpréteur et compilateur),
  sinon les deux chemins divergeraient.
- **Erreurs de calcul unifiées en `JsltError`** : une division par zéro sortait en
  `ZeroDivisionError`, un `+` sur du texte en `ValueError`. L'enveloppe est posée
  dans la **table des opérateurs** (`_BINARY_REPORTED`), que le compilateur
  pré-résout : la poser côté interpréteur seul faisait diverger les deux chemins
  (bug trouvé par le test d'équivalence sur `trydefault`). Les plugins plus
  anciens (`http`, `db`, `elastic`) gardent leurs `ValueError` d'argument :
  unifier serait une rupture, remise à une majeure.
- **Paramètres externes** : `transform/render/debug(..., parameters={...})` et
  `param("nom")` / `params()`. Portés par `RuntimeContext` (3e argument), **pas**
  visibles dans les chemins JSONPath : un réglage n'est pas une donnée du
  document. `param` utilise `.get` pour qu'un paramètre passé explicitement à
  `null` ne soit pas écrasé par son repli.
- `FunctionRegistry.remove(nom)` : pendant de `register`, pour dériver un registre
  restreint (bac à sable) sans le reconstruire de zéro.
- `group` multi-chemins : sous-groupes imbriqués (le .NET les perdait) ; `join` ne
  modifie pas la source (le .NET mutait la gauche) ; `createindex` rend un objet
  `{clé: élément}` (le .NET : `JDictionaryValue` opaque).
- Sortie texte : `$directives.output` (`filter` + `mode`) est appliquée par
  `JsltTemplate.render()` (équivalent `ApplyOutput`) ; `transform()` est inchangé et
  n'émet jamais `$directives` (le .NET non plus — le portage le laissait fuir). Les
  fonctions de sortie (`to_json`, `to_block`, module `functions/outputs.py`) ont le
  `kind="output"` dans le registre : refusées dans le corps du template. Les clés
  `write` (`to_file`) et `to_sqlserver` sont **laissées de côté** (décision
  utilisateur) ; `write` lève `NotImplementedError`. Seule la directive de l'objet
  racine est appliquée ; les autres clés de `$directives` (`culture`…) sont ignorées.
- Casts temporels (`uri`/`uuid`/`datetime`/`time`) rendus en chaîne (simplifié) ;
  `integer`/`decimal`/`string`/`boolean` complets.

## Extensibilité (fonctions & plugins)

Équivalent Python du `ServiceContainer`/`ServiceDiscovery` .NET, rendu idiomatique
(pas de scan d'assembly par réflexion : inutile en Python) :

- **Ajouter** une fonction : décorateur `@jslt_function("nom", path_args=(), description="", kind="function")`
  (analogue de l'attribut `[JsltExtensionMethod]`) ou `registry.register(...)`.
- **Isoler** : `transform(source, functions=mon_registre)` ; `FunctionRegistry()`
  vide ou `default_registry.copy()` pour dériver sans muter le global.
- **Découvrir** : `registry.names()`, `describe(nom) -> FunctionInfo`,
  `describe_all()`, itération, `in` (casse ignorée). `FunctionInfo` porte nom,
  paramètres typés (`ParameterInfo` : nom, type, requis/défaut, `is_path`,
  variadic), type de retour, `path_args`, description, `signature()`.
- **Pour un éditeur (intellisense)** : `registry.catalog()` renvoie une liste de
  dicts **sérialisables JSON** (nom, description, `description_en`, `doc`,
  paramètres nom+type, retour, signature) — analogue du paquet `Intellisense` du
  .NET. `description_en` est la même description en anglais (l'infobulle et la
  page de référence parlent la langue du lecteur) ; `doc` est la page de
  référence, déduite du **module** (`fonctions/<nom>` pour le cœur) et `None`
  ailleurs — un plugin qui héberge sa documentation passe son URL à
  `register(..., doc="https://…")`. Les types proviennent
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

- `packages/urban-json-csv/` — fonctions `loadcsv` / `parsecsv` (port de `ServiceCsv`) et `loadmcsv`
  (CSV multi-enregistrements hiérarchique, port de `ServicesMultiCsv` + `Bb.MultiCsv` ;
  module `urban_json_csv.mcsv`). Distribution `urban-json-csv`, dépend de `urban-json`.
- `packages/urban-json-xml/` — fonctions `loadxml` / `parsexml` (conventions XML↔JSON Newtonsoft du
  `XmlNodeConverter` .NET ; parsing sécurisé via `defusedxml`). Distribution
  `urban-json-xml`, dépend de `urban-json` + `defusedxml`.
- `packages/urban-json-db/` — fonctions `connectsql` / `readsql` (port de `ServicesSql`).
  Distribution `urban-json-db` ; SQLite via la stdlib (sans dépendance), autres SGBD via
  un registre de clients DB-API (extras `postgresql`/`mysql`).
- `packages/urban-json-http/` — fonctions `http` / `httpget` (+ `loadhttpgetjson`,
  compatibilité avec le GET .NET). Appel formalisé en objet
  Fetch/`RequestInit` (`{method,url,headers,query,body}` → `{status,headers,body}`)
  via `httpx`. Distribution `urban-json-http`, dépend de `urban-json` + `httpx`.
- `packages/urban-json-elastic/` — fonctions `esconnect` / `essearch` (recherche
  Elasticsearch → `_source` des hits) via le client officiel `elasticsearch`
  (importé paresseusement). Distribution `urban-json-elastic`, dépend de `urban-json` +
  `elasticsearch`.
- `packages/urban-json-random/` — les 25 fonctions `getrandom_*` (port de
  `Services.randoms.cs`) via Faker + rstr. **Décision : toute génération aléatoire va
  dans ce paquet, jamais dans le cœur.** Bornes `exclusive*` au sens JSON Schema (le
  .NET élargissait l'intervalle). Distribution `urban-json-random`.
- `packages/urban-json-files/` — `loadjson`, `iteratejsonfile` (lecture complète puis
  JSONPath, au lieu du `BigJsonReader` en flux du .NET), `concatpath`. Dépend de
  `urban-json>=0.2.0` (chemins en chaîne).
- `packages/urban-json-html/` — `loadhtml` (fichier ou URL → `{#id, attributs,
  content}` façon HtmlAgilityPack), via `html.parser` de la stdlib.
- `packages/urban-json-excel/` — `loadxls` / `loadxlssheet` (port d'`ExcelReader`) via
  openpyxl ; `.xls` via l'extra `[xls]` (xlrd).
- `packages/urban-json-phone/` — `phoneisvalid` via `phonenumbers` (même
  libphonenumber que le .NET).
- `packages/urban-json-editor/` — composant d'édition **réutilisable** : Web Component
  `<jslt-editor>` (coloration syntaxique + intellisense, **sans dépendance JS**) +
  utilitaires Python (`assets_dir`, `catalog`, `mount`). L'intellisense des fonctions est
  alimentée par `registry.catalog()` ; celle des **chemins** (déclenchée sur `$` et `@`)
  par le document source passé au composant (`ed.source`) **ou** par la liste de chemins
  que calcule l'application hôte (`ed.setPaths`, attribut `paths-url` ; elle prime, et le
  composant ne lit aucun schéma — il replie la liste en arbre et la traverse comme un
  document) — logique pure dans
  `static/jslt-paths.js` (hors DOM, éprouvée sous node : `tests/paths.test.mjs`, rattachée
  à pytest). Les propositions respectent le moteur : pas de projection implicite sur les
  tableaux (`$.items.name` est proposé `$.items[*].name`), portée de l'élément dans un
  filtre `[?(@…)]` et dans une boucle `{"$source": …}`. **Aide à la signature**
  (`static/jslt-signature.js`, pure, `tests/signature.test.mjs`) : dès la
  parenthèse ouvrante, l'appel entourant le caret est rappelé avec le paramètre
  en cours **en gras**, en suivant les virgules — celles d'un tableau ou d'un
  objet appartiennent à leur propre cadre, donc n'avancent pas le paramètre. Elle
  répond à la **position du caret** (clic, flèches) et non à la frappe, sinon
  revenir corriger un argument la laisserait fermée. La signature est un **lien**
  vers `docs/fonctions/<nom>` dans la langue du lecteur (attributs `lang` et
  `docs-base`), construit depuis le champ `doc` du catalogue et **jamais depuis
  le nom** : une fonction de plugin n'a pas de page ici, et un lien fabriqué
  serait mort. Distribution `urban-json-editor`, dépend de `urban-json`.

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
pip install -e packages/urban-json-random
pip install -e packages/urban-json-files packages/urban-json-html
pip install -e packages/urban-json-excel packages/urban-json-phone
pytest packages/urban-json/tests && pytest packages/urban-json-*/tests
ruff check packages
```

## Hors périmètre « cœur » (extensible, non porté)

- Opérateurs ensemblistes de filtre `nin`/`subsetof`/`contains`/`size`/`empty`
  (non implémentés côté .NET non plus). Le filtre `in` **est** porté.
- Fonctions de chemin : `length()` et `value()` **sont** portées (dans les
  chemins et les filtres) ; `count`/`match`/`search` (et `size`, inexistant en
  .NET) lèvent `NotImplementedError`.
- Fonctions d'E-S de fichiers, réseau et base (`loadcsv`, `loadxml`, `loadjson`,
  `loadhtml`, `loadxls`, `http`, `readsql`, `essearch`) et génération aléatoire
  (`getrandom_*`) : hors du cœur **par décision**, elles vivent dans les paquets
  `urban-json-*` (voir « Extensibilité »). Le hachage (`sha256`, `crc32`…) et les
  jointures (`group`, `join`, `index`, `createindex`), eux, **sont** dans le cœur.

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
- maths (`maths.py`) : `abs`, `floor`, `ceil`, `round`, `truncate` (les trois
  arrondis dirigés acceptent une précision), `min`, `max`, `sqrt`, `pow`, `exp`,
  `logarithm`/`10`/`2`, trigonométrie, `pi`, `e`.
- nombres (`numbers.py`) : `parsenumber` (cultures de `format`), `sign`, `clamp`,
  `gcd`, `log` (base libre), `shiftleft`/`shiftright`, `tohex`/`fromhex`,
  `tobase`/`frombase` (2 à 36), `isfinite`, `isnan`.
- texte (`text.py`) : `upper`, `lower`, `trim`, `trimstart`, `trimend`, `split`
  (1er caractère seulement, fidélité .NET), `splitstring` (séparateur entier),
  `startswith`, `endswith`, `stringcontains`, `indexof`, `lastindexof` (texte
  **ou tableau**), `padleft`, `padright`, `stringlenght`, `substring`, `replace`,
  `repeat`, `titlecase`, `shorten`.
- pliage Unicode (`folding.py`, extrait de `text.py`) : `normalize` (formes
  C/D/KC/KD), `deaccent`, `foldtext`, `slugify`.
- proximité (`similarity.py`) : `levenshtein`, `similarity`.
- expressions régulières (`regexes.py`, extrait de `text.py`) : `regexismatch`,
  `regexmatches`, `regexreplace` (substitution .NET `$1`/`${nom}`/`$&` traduite),
  `splitregex`.
- encodage (`encoding.py`) : `tobase64`, `frombase64`, `hexencode`, `hexdecode`,
  `urlencode`, `urldecode`, `htmlescape`, `htmlunescape`, `crc32`, `sha256`,
  `sha512`, `md5`, `sha1`, `hmacsha256`.
- collections (`collection.py`) : `limit`, `skip`, `union`, `flatten`, `select`,
  `selectmany`, `any`, `contains`, `selectany` (`select`/`selectmany`/`selectany`
  prennent un argument-chemin), `zip`, `unzip`, `chunk`, `window`, `partition`,
  `distinctby`, `intersect`, `difference`.
- tri et ordre (`ordering.py`) : `sort` (clef **paresseuse** évaluée par élément,
  ordre total documenté, tri stable, **un sens par clef** possible),
  `reverse`, `first`, `last`.
- agrégats et statistiques (`aggregate.py`) : `count`, `avg`, `median`,
  `product`, `variance`, `stddev` (population par défaut), `percentile`
  (interpolation linéaire), `mode` (toutes valeurs, pas seulement des nombres)
  (+ `min`/`max` sur tableau, dans `maths.py`).
- agrégation par clef calculée (`bykey.py`, extrait d'`aggregate.py`) : `groupby`
  (plat, ou **imbriqué** d'un niveau par clef), `countby`, `sumby`, `avgby`.
- objets (`objects.py`) : `keys`, `values`, `entries`, `fromentries`, `merge`
  (4e argument : concaténer les tableaux), `pick`, `omit`, `has`, `renamekeys`.
- structures profondes (`deep.py`) : `flattenobject`, `unflatten`, `walk`,
  `prune`, `setpath`, `unsetpath`.
- qualité et diagnostic (`quality.py`) : `require`, `requirethat`, `trace`,
  `traces`, `isemail`, `isurl`, `isuuid`, `isiban`.
- types et repli (`types.py`) : `typeof`, `isarray`, `isobject`, `isstring`,
  `isnumber`, `isboolean`, `trydefault` (**arguments paresseux**), `parsejson`.
- regroupement et jointure : `group`, `join`, `index`, `createindex`.
- dates : `parsedate` (culture, masque, fuseau), `dateadd`, `datesub`, `datediff`,
  `datepart`, `datestartof`, `dateendof`, `datezone`, `today`, `dateduration`
  (enregistrement dans `dates.py`, calcul dans `_datecalc.py`, lecture du texte —
  détection, masque, fuseau — dans `_dateread.py`).
- formatage : `format`.
- schéma (`schema.py`) : `schema` (JSON Schema déduit d'un exemple),
  `schemaerrors`, `schemaisvalid` (validation dans `_schemacheck.py`).
- divers : `uuid`, `now`, `isnull`, `isnotnull`, `param`, `params`.
- sortie (`kind="output"`, dans `$directives.output.mode`) : `to_json`,
  `to_block`, `to_csv`, `to_xml`, `to_yaml` (émetteurs sans dépendance dans
  `_writers.py`).

Soit **182 fonctions** dans le registre par défaut (`default_registry.names()` fait
foi ; cette liste est un index, pas la source de vérité). Le `CHANGELOG.md`
détaille ce qui est entré à quelle version.

Quirks .NET conservés : `floor`/`round`/`truncate`/`min`/`max`/`pow`/trig
renvoient un flottant, `round` = arrondi bancaire. `min`/`max` gardent leur forme
binaire .NET (résultat décimal) **et** acceptent un tableau (type conservé) ;
tableau + second argument lève, plutôt que d'ignorer le second.
Hors du cœur : `getrandom_*` et les E-S, qui sont dans les paquets `urban-json-*`.
Non portées nulle part : `write`/`to_file` et `to_sqlserver` (décision utilisateur).

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
- **Une version PyPI est immuable** : la description affichée vient de la
  distribution publiée. Un README corrigé n'atteint donc l'index que par une
  **nouvelle version** — un tag à version identique passe le contrôle
  `tag == __version__` du workflow **puis** échoue à l'upload (« File already
  exists »), run rouge trompeur. Corollaire : une correction de documentation
  destinée aux lecteurs de PyPI vaut un patch.
- Le job **`dist`** de `ci.yml` construit les 12 distributions et passe
  `twine check` à chaque push et chaque PR. C'est le seul endroit qui éprouve ce
  qui part réellement dans une sdist/wheel : le job `test` installe en
  **éditable** et ne voit ni un fichier non versionné, ni une entrée
  `package-data` oubliée (les assets `static/*.js` de l'éditeur n'entrent dans la
  wheel que par là). Sans lui, ces défauts n'apparaissaient qu'au tag de release.
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

- **Documentation bilingue** : toute documentation destinée aux utilisateurs
  existe en **français** (canonique) et en **anglais**, côte à côte —
  `README.md` / `README.en.md`, `docs/guide.md` / `docs/guide.en.md`,
  `CHANGELOG.md` / `CHANGELOG.en.md`, et de même pour chaque paquet et chaque
  application. Les deux portent un bandeau de
  langue sous le titre ; celui des paquets publiés est en **URL absolue**
  (`https://github.com/gaelgael5/Jslt/blob/main/...`), un lien relatif ne
  résolvant pas sur PyPI. Une modification d'un côté n'est pas finie tant que
  l'autre n'est pas à jour. `CLAUDE.md` (instructions d'agent) et
  `ia_instructions/` font exception : français seulement.
- **Guide découpé par thème** : `docs/guide.md` est le **hub** (modèle mental,
  constantes, appel des fonctions, erreurs, aide-mémoire, sommaire) ; chaque
  thème a son document, doublé en anglais — `chemins`, `expressions`,
  `conditions-et-boucles`, `collections`, `objets`, `types`, `nombres`, `texte`,
  `encodage`, `dates`, `sortie`, `extensibilite`, `integration`. Le **nom de fichier reste français** des deux côtés
  (`dates.md` / `dates.en.md`), comme `README.en.md` : le radical identifie le
  document, `.en` la langue. Ajouter un document, c'est l'ajouter dans les deux
  langues, le lier depuis le sommaire du hub et depuis les deux README.
  Trois tests tiennent l'ensemble, parce qu'un lien mort ne se voit pas :
  `test_docs_links.py` (toute ancre et tout chemin relatif de `docs/` résolvent,
  et chaque document a sa traduction), et dans `test_guide_examples.py` l'égalité
  du nombre d'exemples entre les deux langues. Les exemples sont extraits par
  `tests/_docs.py` (partagé avec `test_compiler.py`, qui rejoue tout le guide par
  le chemin compilé) : la liste des fichiers balayés n'existe qu'à cet endroit.
- **Une page de référence par fonction** : `docs/fonctions/<nom>.md` et
  `.en.md` (plus `sommaire.md`), **engendrées** depuis le registre par
  `packages/urban-json/scripts/generate_function_docs.py` ; `tests/test_function_docs.py`
  refuse une page qui ne suit plus le registre, une fonction sans page, sans
  traduction ou sans chapitre. Écrites parce que l'éditeur lie son infobulle à la
  documentation : il lui faut une URL **dérivable du seul nom**, là où une ancre
  dans un chapitre se casse en silence au premier titre renommé. Les exemples et
  la prose restent dans les chapitres, vers lesquels chaque page renvoie ; la
  description, elle, vit dans le registre — c'est là qu'on la corrige. Le
  générateur ne documente que le **cœur** (au module), pour qu'un plugin installé
  dans l'environnement ne peuple pas `docs/fonctions/` de pages que le dépôt ne
  porte pas.
- **Surface d'intégration** : `docs/integration.md` définit trois niveaux de
  garantie — API publique (`urban_json.__all__`, stable), internes **documentés**
  (`parsing`, `runtime`, `ast`, `jsonpath` : non figés mais tout mouvement est
  annoncé au `CHANGELOG`), et le reste (aucune garantie). Écrit parce qu'une
  intégration s'y branchait et devait comparer les sources de deux versions octet
  par octet pour valider une montée. `tests/test_integration_surface.py` épingle
  cette surface : si un nom documenté disparaît, la suite rougit là.
- **Journal des modifications** : `CHANGELOG.md` / `.en.md`, par version, pour le
  cœur **et** les plugins, avec les mouvements des internes documentés. Il
  n'existait pas ; une montée de version se validait en lisant les sources.
- snake_case côté code maison ; les overrides du visiteur ANTLR restent en
  camelCase (API imposée par le générateur).
- Toute fonctionnalité portée s'accompagne de tests, dont, quand c'est possible,
  des cas repris de `Black.Beard.Jslt.UnitTests` comme oracle de conformité.
- Les constructions non encore portées lèvent `NotImplementedError` avec un
  message explicite plutôt que de produire un résultat faux.
