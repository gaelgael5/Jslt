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
