# Guide jslt — langage de transformation JSON → JSON

*Français · [English](guide.en.md)*

Ce guide présente **chaque construction du langage** avec des exemples. Tous les
exemples sont **exécutés par la suite de tests** (`tests/test_guide_examples.py`)
sous la forme de triplets *template → entrée → sortie* : ils sont donc toujours
exacts et à jour.

Pour les reproduire :

```python
from urban_json import JsltTemplate
JsltTemplate.parse(TEMPLATE).transform(ENTREE)   # == SORTIE
```

> **Convention de lecture.** Dans chaque exemple, le premier bloc est le
> **template** jslt, le deuxième l'**entrée** (document source JSON), le troisième
> la **sortie** attendue.

---

## Table des matières

**Le langage**

- [Modèle mental](#modèle-mental) · [Constantes et structure](#constantes-et-structure)
- [Chemins JSONPath](chemins.md) — accès par clé, indice, slice,
  wildcard, descente `..`, sémantique 0 / 1 / N, filtres `?(...)`, `length()` / `value()`
- [Expressions](expressions.md) — variables, opérateurs, coalescence `??`,
  casts `#type`, chaînage `->`
- [Conditions et boucles](conditions-et-boucles.md) — `when` / `switch`,
  `$source` / `$where`

**Les fonctions intégrées** — comment on les appelle :
[Fonctions intégrées](#fonctions-intégrées)

- [Données et collections](collections.md) — `sum`, `distinct`, `limit`, `skip`,
  `union`, `flatten`, `select`, `selectmany`, `zip`, `unzip`, `chunk`, `window`,
  `partition`, `distinctby`, `intersect`, `difference`, `group`, `groupby`,
  `countby`, `sumby`, `avgby`, `join`, `index`, `sort`, `reverse`, `first`,
  `last`, `count`, `avg`, `median`, `product`, `variance`, `stddev`,
  `percentile`, `mode`
- [Objets et structures profondes](objets.md) — `keys`, `values`, `entries`,
  `fromentries`, `merge`, `pick`, `omit`, `has`, `renamekeys`,
  `flattenobject`, `unflatten`, `walk`, `prune`, `setpath`, `unsetpath`
- [Types, repli sur erreur et validation](types.md) — `typeof`, `isarray`,
  `isobject`, `isstring`, `isnumber`, `isboolean`, `trydefault`, `parsejson`,
  `schema`, `schemaerrors`, `schemaisvalid`
- [Nombres et maths](nombres.md) — `min`, `max`, `abs`, `floor`, `ceil`, `round`,
  `sqrt`, `log`, `parsenumber`, `sign`, `clamp`, `gcd`, `tobase`, `isfinite`…
- [Texte, expressions régulières et formatage](texte.md) — `upper`, `split`,
  `splitstring`, `splitregex`, `substring`, `replace`, `regexreplace`, `shorten`,
  `slugify`, `levenshtein`, `similarity`, `foldtext`, `deaccent`, `normalize`,
  `format`
- [Encodage, empreintes et échappement](encodage.md) — `tobase64`, `sha256`,
  `hmacsha256`, `urlencode`, `htmlescape`, `hexencode`…
- [Dates et heures](dates.md) — `parsedate` (culture, masque, fuseau), `dateadd`,
  `datesub`, `datediff`, `datepart`
- [Sortie texte](sortie.md) — `to_json`, `to_block`, `to_csv`, `to_xml`,
  `to_yaml`, `$directives.output`
- [Qualité : refuser, observer, valider](qualite.md) — `require`, `requirethat`,
  `trace`, `traces`, `isemail`, `isurl`, `isuuid`, `isiban`

**Référence**

- [Toutes les fonctions, une page chacune](fonctions/sommaire.md) — signature,
  arguments et description, engendrées depuis le registre. C'est là que mène
  l'infobulle de l'éditeur ; les exemples, eux, restent dans les chapitres
  ci-dessus.

**Autour du langage**

- [Extensibilité, débogage et re-sérialisation](extensibilite.md) — registre de
  fonctions, plugins par entry points, pas à pas, `to_source()`
- [Erreurs](#erreurs) · [Aide-mémoire](#aide-mémoire)

---

## Modèle mental

Un template jslt **ressemble** à du JSON, mais les *valeurs* sont des
**expressions** évaluées contre le document source. La racine du document source
est désignée par `$`.

- La **structure** du template (objets, tableaux, clés) décrit la forme de la
  sortie.
- Les **valeurs** (`$.x`, `sum(...)`, `$.a + $.b`…) sont calculées.

Une valeur littérale se recopie telle quelle :

```jslt
{ "ville": "Paris", "pays": "FR" }
```
```json
{}
```
```json
{ "ville": "Paris", "pays": "FR" }
```

---

## Constantes et structure

Les quatre types scalaires JSON sont des constantes directes :

```jslt
{ "i": 6, "d": 6.7, "b": true, "z": null }
```
```json
{}
```
```json
{ "i": 6, "d": 6.7, "b": true, "z": null }
```

Objets et tableaux s'imbriquent librement :

```jslt
{ "meta": { "actif": true }, "codes": [1, 2, 3] }
```
```json
{}
```
```json
{ "meta": { "actif": true }, "codes": [1, 2, 3] }
```

---

## Fonctions intégrées

Les fonctions s'appellent par nom : `fonction(arg1, arg2, ...)`. Chaque argument
est une expression évaluée.

Un argument peut être **paresseux** : la fonction l'évalue elle-même, quand elle
veut et contre la source qu'elle choisit. C'est ce qui permet à `sort` de
calculer une clef **par élément** et à `trydefault` de n'évaluer son repli que si
le premier calcul échoue. Cela ne change rien à l'écriture d'un appel.

> Toutes les fonctions ne sont pas illustrées ici : la trigonométrie
> (`sin`, `cos`…) suit les mêmes conventions que les autres fonctions
> numériques, et `uuid()`, `now()`, `today()` sont non déterministes. La liste
> complète fait foi dans `default_registry.names()` ; l'éditeur et le playground
> la lisent directement.

Pour appeler le moteur depuis du code — y compris ses pièces internes — voir
[Intégrer le moteur](integration.md).

---

## Erreurs

Un template syntaxiquement invalide lève `JsltSyntaxError` (avec ligne/colonne) :

```python
from urban_json import JsltTemplate, JsltSyntaxError

try:
    JsltTemplate.parse('{ "n": ~ }')
except JsltSyntaxError as e:
    print(e.line, e.column)   # position de l'erreur
```

Une construction reconnue par la grammaire mais **non portée** (ex. opérateur de
filtre `contains`, fonction de chemin `size()`) lève `NotImplementedError` avec un
message explicite — jamais un résultat faux :

```python
from urban_json import JsltTemplate

JsltTemplate.parse('{ "r": $.a[?(@.x contains 1)] }')   # -> NotImplementedError
```

---

## Aide-mémoire

| Construction | Syntaxe | Section |
|---|---|---|
| Chemin | `$.a.b`, `$.l[0]`, `$.l[1:3]`, `$.*`, `$..k` | [Chemins](chemins.md#lire-la-source) |
| Variable | `"v:": expr`, `v:`, `v:$.x` | [Expressions](expressions.md#variables) |
| Arithmétique | `+ - * / %` | [Expressions](expressions.md#opérateurs) |
| Comparaison | `== != < <= > >=` | [Expressions](expressions.md#opérateurs) |
| Logique booléenne | `&& \|\| !` | [Expressions](expressions.md#opérateurs) |
| Bit-à-bit / XOR | `& \| ^` | [Expressions](expressions.md#opérateurs) |
| Coalescence | `a ?? b` | [Expressions](expressions.md#coalescence--et-valeurs-manquantes) |
| Fonction | `f(a, b)` | [Fonctions](#fonctions-intégrées) |
| Cast | `expr #integer` | [Expressions](expressions.md#casts-type) |
| Chaînage | `expr -> f()` | [Expressions](expressions.md#chaînage--) |
| Condition | `when(e) { "c": v, "default": d }` | [Boucles](conditions-et-boucles.md#when--switch) |
| Boucle | `[ { "$source": $.l, "$where": c, ... } ]` | [Boucles](conditions-et-boucles.md#boucles-source--where) |
| Filtre | `$.l[?(@.x > 1 & @.y in [..])]` | [Chemins](chemins.md#filtres-jsonpath-) |
| Fonction de chemin | `$.x.length()`, `$.x.value()` | [Chemins](chemins.md#fonctions-de-chemin-length--value) |
| Paramètre externe | `param("lot", "defaut")` | [Expressions](expressions.md#paramètres-externes-param-params) |
| Repli sur erreur | `trydefault(expr, repli)` | [Types](types.md#repli-sur-erreur--trydefault) |
| Refus explicite | `require($.x, "message")` | [Qualité](qualite.md#refuser--require-requirethat) |
| Observation | `trace($.x, "étiquette")` | [Qualité](qualite.md#observer--trace-traces) |
| Tri | `sort($.l, $.k, true)` | [Collections](collections.md#trier-et-ordonner-sort-reverse-first-last) |
| Total par groupe | `sumby($.l, $.k, $.v)` | [Collections](collections.md#agréger-par-groupe-groupby-countby-sumby-avgby) |

Pour l'architecture interne, les patterns de portage et les écarts volontaires
vis-à-vis du .NET, voir [`CLAUDE.md`](../CLAUDE.md).

