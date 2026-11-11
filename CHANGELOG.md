# Journal des modifications

*Français · [English](CHANGELOG.en.md)*

Ce journal couvre le **cœur** (`urban-json`) et les paquets `urban-json-*` du
dépôt. Il note aussi les mouvements des **internes documentés**
(`urban_json.parsing`, `runtime`, `ast`, `jsonpath`) : ils ne sont pas figés,
mais une intégration qui s'y branche doit pouvoir lire ici ce qui a bougé plutôt
que de comparer deux versions ligne à ligne. Les trois niveaux de garantie sont
décrits dans [Intégrer le moteur](docs/integration.md).

Versions selon [SemVer](https://semver.org/lang/fr/) ; une version PyPI est
immuable, une correction de documentation destinée à l'index vaut donc un patch.

## urban-json-editor 0.4.0 — 2026-11-11

### Ajouté

- **Aide à la signature.** Dès la parenthèse ouvrante, l'appel qui entoure le
  caret est rappelé avec le **paramètre en cours de saisie en gras**, et il suit
  les virgules — la liste de propositions, elle, disparaissait à la première
  virgule et ne disait jamais *où* l'on en était. Les virgules d'un tableau ou
  d'un objet n'avancent pas le paramètre (`sort($.l, [$.a, $.b], …)` reste au
  2ᵉ), et un argument en trop ne met rien en gras plutôt que de désigner un
  paramètre au hasard.
- **L'aide suit le caret, pas la frappe** : cliquer dans les parenthèses d'un
  appel déjà écrit la rouvre, de même que les flèches. C'est le geste de qui
  revient corriger un argument, et il ne produit aucun `input`.
- **La signature est un lien** vers la page de référence de la fonction, dans la
  langue du lecteur (attribut `lang`, sinon celui du document, sinon le
  navigateur) et sous la racine de son choix (attribut `docs-base`). L'URL vient
  du champ `doc` du catalogue : une fonction de plugin, qui n'a pas de page dans
  ce dépôt, s'affiche sans lien plutôt qu'avec un lien mort. L'infobulle et la
  liste de propositions suivent la même langue (`description_en`).
- Nouvel asset `jslt-signature.js` (logique pure, éprouvée sous node) : il
  s'ajoute à `ASSET_FILES` et doit être servi avec les autres.

## urban-json 0.6.0 — 2026-11-11

Quatre catégories comblées (162 → 182) et un défaut de sortie corrigé.

### Corrigé

- **Du `repr` Python pouvait sortir dans le JSON produit.** `to_text` rendait
  `str(valeur)` pour un tableau ou un objet, donc la représentation *Python*,
  guillemets simples compris : `concat($.l, ",")` sur `[[1,"x"], 2]` rendait
  `"[1, 'x'],2"`, et une clef composite de `groupby` / `countby` donnait
  `"[1, 'x']"`. Le cast `#string` passait, lui, par le JSON : deux chemins de
  mise en texte coexistaient, l'un correct et l'autre non. Il n'en reste qu'un,
  celui du JSON compact — qui est aussi ce que rend `token.ToString()` côté
  Newtonsoft.

### Ajouté — 20 fonctions

- **Structures profondes** : `flattenobject`, `unflatten` (les segments
  numériques ne redeviennent des tableaux que sur demande : une clé « 2026 » est
  un nom d'année dans bien des documents), `walk` (des feuilles vers la racine,
  pour qu'une règle dépendant des enfants fonctionne), `prune`, `setpath`,
  `unsetpath`.
- **Sortie** : `to_csv` (RFC 4180, colonnes = union des clés, valeurs imbriquées
  aplaties en clés pointées), `to_xml` (conventions de `parsexml` : `@attribut`,
  `#text`, tableau = élément répété), `to_yaml` (style bloc ou style JSON ;
  sous-ensemble assumé, sans ancres ni tags). Les trois sont **sans dépendance**.
- **Qualité et diagnostic** : `require` (exige une valeur **présente** : `0`,
  `false` et `""` sont des valeurs), `requirethat` (exige une condition
  strictement vraie), `trace` / `traces` (observer sans polluer la sortie ; le
  journal vit sur le contexte, donc deux exécutions ne se mélangent jamais), et
  les validateurs `isemail`, `isurl`, `isuuid`, `isiban` (structure **et** clé
  modulo 97).
- **Une page de référence par fonction**, dans les deux langues
  (`docs/fonctions/<nom>.md` et `.en.md`, plus un sommaire) : signature,
  arguments et description, **engendrées** depuis le registre par
  `packages/urban-json/scripts/generate_function_docs.py` — une recopie à la
  main aurait vieilli dès la première signature élargie, et un test refuse une
  page qui ne suit plus le registre. C'est l'URL stable que l'éditeur peut
  dériver du seul nom de la fonction, là où une ancre dans un chapitre se casse
  en silence au premier titre renommé. Les exemples et la prose restent dans les
  chapitres.
- **Toutes les descriptions sont traduites** (`description_en`) : la page
  anglaise n'a pas d'autre source, et l'intellisense parle désormais la langue
  du lecteur.
- **Tri et regroupement, les finitions** : `unzip` (réciproque de `zip`, qui n'en
  avait pas), `sumby` et `avgby` (le total par groupe demandait quatre fonctions
  imbriquées pour l'usage le plus fréquent du regroupement ; la valeur agrégée
  est paresseuse, omise elle vaut l'élément, et une valeur non numérique lève
  comme pour `sum`).

### Modifié — signature élargie, compatible

- `merge(a, b, deep, arrays)` : 4e argument pour **concaténer** les tableaux au
  lieu de les remplacer. Le remplacement reste le défaut, fusionner deux listes
  de longueurs différentes n'ayant pas de sens unique.
- `sort(l, clef, descendant)` : `descendant` accepte un **tableau de booléens**,
  un sens par clef (`sort($.l, [$.a, $.b], [true, false])`). Le booléen unique
  reste valable et inchangé. Un sens manquant vaut croissant ; un sens **en trop
  lève**, parce que c'est la faute d'écriture la plus probable et qu'elle
  laisserait un tri d'apparence juste. Cette forme compare composante par
  composante, donc un peu plus lentement — elle seule.
- `groupby(l, clef, nested)` : 3e argument pour **imbriquer** un niveau d'objet
  par clef, au lieu de la clef textuelle `["FR","Lyon"]` qu'il fallait
  re-analyser. La forme plate reste le défaut. Imbriquer exige le même nombre de
  clefs pour tous les éléments : sinon une même clef porterait des éléments *et*
  un sous-groupe, et l'un des deux disparaîtrait — ce cas lève.

### Internes documentés

- `FunctionInfo` porte `description_en` (la même description en anglais) et
  `doc` (la page de référence, `"fonctions/<nom>"` pour le cœur, `None` pour une
  fonction dont ce dépôt ne porte pas la page). Les deux sont dans
  `catalog()` : c'est de là que l'éditeur tire l'infobulle et son lien.
  `register()` et `jslt_function()` les acceptent en arguments nommés, à la fin
  — un appel existant est inchangé.
- `RuntimeContext` porte désormais `traces` (liste des observations), lisible par
  un intégrateur après l'exécution. Attribut ajouté, rien n'est retiré.
- Nouveaux modules internes : `functions/deep.py`, `functions/quality.py`,
  `functions/_writers.py` (les trois émetteurs), `functions/bykey.py`.
- `groupby` et `countby` ont quitté `functions/aggregate.py` pour
  `functions/bykey.py`, avec `sumby` et `avgby` : elles partagent une clef
  calculée par élément, pas la convention des agrégats. Aucun changement pour un
  template (le registre résout par **nom**) ; seul un import direct du module
  est concerné.

### Toujours pas traité

- **Dates** : `fromunix` / `tounix` (et `convert(x, "datetime")` rend encore
  l'epoch en **texte**, ce qui ressemble à une date sans en être une), durées ISO
  8601, `daterange`.
- **Sécurité** : chiffrement, JWT, base32, `uuid` v5/v7, masquage.
- **Tri** : pas de `minby` / `maxby` (l'élément qui porte l'extremum) ; le
  classement par rang (`rank`) n'existe pas non plus.
- **Langage** : fonctions définies dans le template, inclusion, interpolation de
  chaînes — grammaire ANTLR, Java requis.

## urban-json 0.5.0 — 2026-11-11

Corrige un tri faux et comble quatre catégories de fonctions (135 → 162).

### Corrigé

- **Tri multi-clefs faux sur les nombres.** L'ordre total comparait tableaux et
  objets par leur **JSON compact**, donc par points de code : `sort($.l, [$.a,
  $.b])` — l'usage naturel d'une clef, puisque c'est une expression qui peut
  rendre un tableau — plaçait `[10]` avant `[2]`. Les tableaux sont désormais
  comparés **élément par élément** (un préfixe passe devant la séquence qu'il
  préfixe) et les objets par leurs clés triées puis leurs valeurs. Invisible
  tant qu'on triait des scalaires ; silencieusement faux sinon.

### Ajouté — 27 fonctions

- **Collections** : `skip` (le complément de `limit`, sans lequel il n'y avait
  pas de pagination), `flatten` (récursif, là où `union` ne descend que d'un
  niveau), `zip`, `chunk`, `window`, `partition`, `distinctby`, `intersect`,
  `difference`.
- **Statistiques** : `variance`, `stddev` (population par défaut),
  `percentile` (interpolation linéaire, donc `percentile(v, 50)` coïncide avec
  `median`), `mode` (sur toutes valeurs, pas seulement des nombres), `groupby`
  (en **objet**, donc réductible par `entries`), `countby`.
- **Texte** : `splitstring` (séparateur **entier** : `split` ne retient que son
  premier caractère, fidélité .NET), `splitregex`, `shorten` (ellipse, suffixe
  compris dans la longueur, coupe au dernier espace), `slugify`, `levenshtein`,
  `similarity`.
- **Nombres** : `ceil` (`floor` existait seul), `log` à base libre, `tobase` /
  `frombase` (2 à 36), `isfinite`, `isnan`.

### Modifié — signatures élargies, compatibles

- `indexof` / `lastindexof` acceptent un **tableau** (position, ou `-1`). Sur un
  tableau, l'égalité est **structurelle** : chercher `2` ne trouve pas `"2"`,
  là où `contains` garde l'égalité `==` du langage par fidélité .NET.
- `reverse` accepte une **chaîne** (il rendait `null`) et travaille par
  graphème : sur un « é » décomposé, inverser les points de code collerait
  l'accent sur la lettre voisine.
- `floor`, `ceil` et `truncate` acceptent une précision en décimales.

### Modifié — comportement

- `log(1000, 10)` rend exactement `3.0` : les bases 10 et 2 passent par leur
  fonction dédiée, parce que diviser deux logarithmes rend `2.9999999999999996`
  — un nombre qui ressortirait tel quel dans le JSON produit.

### Internes documentés

- `functions/folding.py` (pliage Unicode) et `functions/similarity.py` extraits
  de `text.py`, `functions/_lazy.py` partagé par toutes les fonctions à clef
  calculée. Ce sont des modules internes non documentés : aucune garantie, mais
  c'est noté ici parce que le découpage de `functions/` sert de carte.

## urban-json 0.4.0 — 2026-11-11

Comble onze familles de fonctions manquantes. **Aucune rupture** : rien n'est
retiré ni renommé, les signatures existantes gagnent des arguments optionnels.

### Ajouté — 60 fonctions (75 → 135)

- **Chaînes** : `substring`, `replace`, `regexreplace`, `trimstart`, `trimend`,
  `repeat`, `titlecase`.
- **Unicode** : `deaccent`, `foldtext` (clé de comparaison : casse et/ou
  accents).
- **Tri et ordre** : `sort` (clef calculée par élément, ordre total documenté,
  tri stable), `reverse`, `first`, `last`.
- **Agrégats** : `count`, `avg`, `median`, `product`.
- **Objets** : `keys`, `values`, `entries`, `fromentries`, `merge`, `pick`,
  `omit`, `has`, `renamekeys`.
- **Types** : `typeof`, `isarray`, `isobject`, `isstring`, `isnumber`,
  `isboolean`.
- **Repli sur erreur** : `trydefault` (n'évalue son repli que si l'expression
  lève, et ne rattrape **pas** `NotImplementedError`).
- **Validation** : `schemaerrors`, `schemaisvalid` (sous-ensemble JSON Schema
  documenté ; les mots-clés inconnus sont ignorés, pas refusés).
- **Lecture de JSON** : `parsejson`.
- **Nombres** : `parsenumber` (cultures de `format`), `sign`, `clamp`, `gcd`,
  `shiftleft`, `shiftright`, `tohex`, `fromhex`.
- **Dates** : `datestartof`, `dateendof`, `datezone`, `today`, `dateduration`.
- **Encodage et empreintes** : `md5`, `sha1`, `hmacsha256`, `urlencode`,
  `urldecode`, `htmlescape`, `htmlunescape`, `hexencode`, `hexdecode`.
- **Paramètres externes** : `param`, `params`.

### Modifié — signatures élargies, compatibles

- `min(tableau)` / `max(tableau)` agrègent, en plus de leur forme binaire .NET
  (qui garde son résultat décimal). Un tableau **et** un second argument lève,
  plutôt que d'ignorer le second.
- `round(v, décimales)` : précision optionnelle, arrondi bancaire conservé.
- `normalize(v, forme)` : `C` (défaut), `D`, `KC`, `KD`.
- `datepart` : nouvelles parties `quarter`, `week` (ISO), `dayofyear`,
  `millisecond`.
- `dateadd` / `datesub` / `datediff` : nouvelle unité `weekday` (jours ouvrés
  lundi-vendredi, **sans** calendrier de jours fériés).

### Modifié — comportement

- **Les erreurs de calcul sont désormais des `JsltError`.** Une division par
  zéro sortait en `ZeroDivisionError`, un `+` sur du texte en `ValueError` :
  illisibles dans un message et impossibles à rattraper depuis un template.
  Elles restent des exceptions, mais de la famille du moteur. Un appelant qui
  attrapait `ZeroDivisionError` ou `ValueError` **spécifiquement** doit passer à
  `JsltError` ; attraper `Exception` ne change pas.
- **Le chemin compilé et l'interpréteur ne divergent plus sur les erreurs.** Le
  compilateur pré-résout les opérateurs et appelait la callable brute : la même
  division par zéro levait une `ZeroDivisionError` en compilé et une `JsltError`
  en interprété. L'enveloppe est passée dans la table des opérateurs, que les
  deux chemins partagent.

### Ajouté — API

- `transform(source, functions=…, parameters=…)`, idem `render` et `debug` :
  réglages externes lus par `param("nom")`. Ils ne sont **pas** visibles dans
  les chemins JSONPath.
- `FunctionRegistry.remove(nom)` : pendant de `register`, pour dériver un
  registre restreint sans le reconstruire.
- `@jslt_function(..., lazy_args=(…))` et `FunctionRegistry.lazy_args_of` :
  arguments reçus non évalués, que la fonction appelle quand elle veut (c'est le
  mécanisme de `sort` et de `trydefault`). Le catalogue expose `lazy_args`.

### Internes documentés

- `urban_json.parsing` exporte désormais `ScriptBuilderVisitor` (il n'était
  atteignable que par son module). `parse_to_tree` est inchangé.
- `RuntimeContext(sources, functions, parameters)` : **troisième argument
  ajouté**, optionnel et positionnel — un appel existant à deux arguments reste
  valide.
- `ast`, `jsonpath` : inchangés.

### Documentation

- Guide découpé par thème (10 → 13 documents par langue) ; trois nouveaux :
  [Objets](docs/objets.md), [Types et validation](docs/types.md),
  [Encodage](docs/encodage.md) — ce dernier documente aussi `tobase64`,
  `crc32`, `sha256` et `sha512`, qui ne l'étaient nulle part.
- [Intégrer le moteur](docs/integration.md) : les trois surfaces et leur
  garantie, le pipeline pièce par pièce, et comment restreindre les fonctions.
- Ce journal, qui n'existait pas.

### Plugins

- `urban-json-xml 0.2.0` : `parsexml(texte)` — la conversion de `loadxml` depuis
  une chaîne.
- `urban-json-csv 0.2.0` : `parsecsv(texte, …)` — la lecture de `loadcsv` depuis
  une chaîne, mêmes options.
- Les deux lèvent `JsltError` (famille du moteur, rattrapable par `trydefault`),
  là où les fonctions de fichier plus anciennes gardent `ValueError`. L'écart
  est connu ; l'unifier serait une rupture, remise à une version majeure.

### Non traité, et pourquoi

- **Fonctions définies dans le template** (lambda, macro, récursion) et
  **inclusion d'un autre template** : demandent une nouvelle syntaxe, donc une
  modification de la grammaire ANTLR et sa régénération (Java requis). Aucune
  fonction ne les contourne.
- **YAML** : demanderait une dépendance et une distribution de plus
  (`urban-json-yaml`) ; c'est une décision de périmètre, pas un oubli.
- **Tri par collation locale** et **translittération** : demandent ICU. En
  attendant, trier sur une clé `foldtext` donne un ordre humain pour les langues
  à diacritiques latins.

## urban-json 0.3.0 — 2026-11-10

Documenté après coup : ce journal n'existait pas, et l'annonce du tag disait
« aucune rupture » sans détailler.

### Ajouté

- `parsedate(texte, culture, masque, fuseau)` : 3e argument **masque** (lecture
  stricte selon le vocabulaire .NET de `format`) et 4e argument **fuseau** (nom
  IANA, `UTC`/`Z`, décalage fixe ; il attribue à une date naïve, convertit une
  date décalée).
- `dateadd`, `datesub`, `datediff`, `datepart` (71 → 75 fonctions).

### Modifié — comportement de fonctions existantes

Trois changements que l'annonce ne mentionnait pas :

- **`parsedate` a été entièrement réécrite.** Une composante absente du masque
  vaut l'époque Unix, pas « aujourd'hui » comme en .NET : le résultat d'un
  template ne doit pas dépendre du jour d'exécution.
- **`format` lit désormais une chaîne ISO suffixée `Z`** comme une date. Elle
  ressortait brute avant : une sortie peut donc **changer silencieusement** sur
  ce cas précis.
- **`format` écrit les jetons de fuseau `z`, `zz`, `zzz`, `K`**, qui levaient.
  Sur une date sans décalage, `z` écrit zéro — le .NET prendrait celui de la
  machine, et une sortie ne doit pas dépendre du serveur.

### Internes

`parsing/`, `ast/`, `runtime/`, `jsonpath/` et `serialization.py` sont
**identiques à 0.2.1**. Seuls cinq fichiers de `functions/` changent. C'est ce
qui autorisait la montée de version sans relire chaque visiteur — et c'est
précisément ce qu'une intégration avait dû établir elle-même, en comparant les
sources.

## Avant 0.3.0

Pas de journal. L'historique git fait foi ; les jalons publiés sont
`urban-json` 0.1.0, 0.2.0 et 0.2.1, et `urban-json-editor` 0.1.1 → 0.3.0.
