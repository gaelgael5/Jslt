# Guide jslt — langage de transformation JSON → JSON

*Français · [English](guide.en.md)*

Ce guide présente **chaque construction du langage** avec des exemples. Tous les
exemples sont **exécutés par la suite de tests** (`tests/test_guide_examples.py`)
sous la forme de triplets *template → entrée → sortie* : ils sont donc toujours
exacts et à jour.

Pour les reproduire :

```python
from jslt import JsltTemplate
JsltTemplate.parse(TEMPLATE).transform(ENTREE)   # == SORTIE
```

> **Convention de lecture.** Dans chaque exemple, le premier bloc est le
> **template** jslt, le deuxième l'**entrée** (document source JSON), le troisième
> la **sortie** attendue.

---

## Table des matières

1. [Modèle mental](#1-modèle-mental)
2. [Constantes et structure](#2-constantes-et-structure)
3. [JSONPath : lire la source](#3-jsonpath--lire-la-source)
4. [Sémantique 0 / 1 / N](#4-sémantique-0--1--n)
5. [Variables](#5-variables)
6. [Opérateurs](#6-opérateurs)
7. [Coalescence `??` et valeurs manquantes](#7-coalescence--et-valeurs-manquantes)
8. [Fonctions intégrées](#8-fonctions-intégrées)
9. [Casts `#type`](#9-casts-type)
10. [Chaînage `->`](#10-chaînage--)
11. [`when` / `switch`](#11-when--switch)
12. [Boucles `$source` / `$where`](#12-boucles-source--where)
13. [Filtres JSONPath `?(...)`](#13-filtres-jsonpath-)
14. [Fonctions de chemin `length()` / `value()`](#14-fonctions-de-chemin-length--value)
15. [Re-sérialisation `to_source()`](#15-re-sérialisation-to_source)
16. [Extensibilité : fonctions et plugins](#16-extensibilité--fonctions-et-plugins)
17. [Débogage (pas à pas)](#17-débogage-pas-à-pas)
18. [Erreurs](#18-erreurs)
19. [Aide-mémoire](#19-aide-mémoire)

---

## 1. Modèle mental

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

## 2. Constantes et structure

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

## 3. JSONPath : lire la source

`$` est la racine du document source. On navigue avec `.clé`, `[indice]`,
`[début:fin]` (slice), `*` (wildcard) et `..` (descente récursive).

### Accès par clé

```jslt
{ "nom": $.user.name, "age": $.user.age }
```
```json
{ "user": { "name": "Alice", "age": 30 } }
```
```json
{ "nom": "Alice", "age": 30 }
```

### Indice, slice, wildcard

```jslt
{ "premier": $.items[0], "slice": $.items[1:3], "wild": $.obj.* }
```
```json
{ "items": [10, 20, 30, 40], "obj": { "x": 1, "y": 2 } }
```
```json
{ "premier": 10, "slice": [20, 30], "wild": [1, 2] }
```

### Descente récursive `..`

`$..id` collecte **tous** les `id`, à n'importe quelle profondeur, dans l'ordre
de parcours du document (un nœud est inspecté avant ses enfants) :

```jslt
{ "ids": $..id }
```
```json
{ "a": { "id": 1 }, "b": { "nested": { "id": 2 } }, "c": { "id": 3 } }
```
```json
{ "ids": [1, 2, 3] }
```

---

## 4. Sémantique 0 / 1 / N

Un chemin (ou un filtre) peut sélectionner **0, 1 ou N** valeurs. Le résultat
suit la règle du moteur .NET (`GetContentByJPath`) :

| Correspondances | Résultat |
|---|---|
| 0 | `null` |
| 1 | la valeur (pas une liste d'un élément) |
| N | la liste des valeurs |

Zéro correspondance → `null` :

```jslt
{ "r": $.inconnu }
```
```json
{ "a": 1 }
```
```json
{ "r": null }
```

Une seule correspondance → la valeur directement :

```jslt
{ "r": $.items[?(@.n == 2)] }
```
```json
{ "items": [ { "n": 1 }, { "n": 2 }, { "n": 3 } ] }
```
```json
{ "r": { "n": 2 } }
```

Plusieurs correspondances → une liste :

```jslt
{ "r": $.items[?(@.n >= 2)] }
```
```json
{ "items": [ { "n": 1 }, { "n": 2 }, { "n": 3 } ] }
```
```json
{ "r": [ { "n": 2 }, { "n": 3 } ] }
```

---

## 5. Variables

Une **déclaration** de variable est une clé terminée par `:` (par ex. `"u:"`).
Sa valeur est évaluée une fois, puis réutilisable par **référence** `nom:` ou par
**projection** `nom:$.chemin` (le chemin est alors appliqué *à la variable*).
Les clés-déclarations ne figurent pas dans la sortie.

```jslt
{ "u:": $.user, "nom": u:$.name, "ville": u:$.city }
```
```json
{ "user": { "name": "Bob", "city": "Lyon" } }
```
```json
{ "nom": "Bob", "ville": "Lyon" }
```

Référence simple (sans projection) :

```jslt
{ "v:": 42, "copie": v: }
```
```json
{}
```
```json
{ "copie": 42 }
```

---

## 6. Opérateurs

### Arithmétique `+ - * / %`

La division **entière** est tronquée vers zéro (comportement C#) ; dès qu'une
opérande est décimale, la division est réelle.

```jslt
{ "add": $.a + $.b, "sub": $.a - $.b, "mul": $.a * $.b, "div": $.a / $.b, "mod": $.a % $.b }
```
```json
{ "a": 17, "b": 5 }
```
```json
{ "add": 22, "sub": 12, "mul": 85, "div": 3, "mod": 2 }
```

```jslt
{ "div_reelle": $.a / $.b }
```
```json
{ "a": 17.0, "b": 5 }
```
```json
{ "div_reelle": 3.4 }
```

### Comparaison `== != < <= > >=`

```jslt
{ "eq": $.a == $.b, "lt": $.a < $.b, "ge": $.a >= $.b }
```
```json
{ "a": 3, "b": 4 }
```
```json
{ "eq": false, "lt": true, "ge": false }
```

### Logique booléenne `&& || !`

```jslt
{ "et": $.x && $.y, "ou": $.x || $.y, "non": !$.x }
```
```json
{ "x": true, "y": false }
```
```json
{ "et": false, "ou": true, "non": false }
```

### Bit-à-bit `&` `|` et XOR `^`

Attention : fidèlement au .NET, `&`/`|` sont les opérateurs **bit-à-bit entiers**
(et non booléens — ceux-ci sont `&&`/`||`), et `^` est le **XOR entier**.

```jslt
{ "bitand": $.a & $.b, "bitor": $.a | $.b, "xor": $.a ^ $.b }
```
```json
{ "a": 6, "b": 3 }
```
```json
{ "bitand": 2, "bitor": 7, "xor": 5 }
```

---

## 7. Coalescence `??` et valeurs manquantes

`a ?? b` renvoie `a` s'il n'est pas `null`, sinon `b`. Combiné à la sémantique
« 0 correspondance → null », c'est le moyen idiomatique de donner une valeur par
défaut à un champ absent.

```jslt
{ "ville": $.user.city ?? "inconnue" }
```
```json
{ "user": { "name": "Z" } }
```
```json
{ "ville": "inconnue" }
```

Si la valeur existe, elle l'emporte :

```jslt
{ "ville": $.user.city ?? "inconnue" }
```
```json
{ "user": { "city": "Nantes" } }
```
```json
{ "ville": "Nantes" }
```

---

## 8. Fonctions intégrées

Les fonctions s'appellent par nom : `fonction(arg1, arg2, ...)`. Chaque argument
est une expression évaluée.

### Cœur : `sum`, `concat`, `distinct`

`sum` additionne les éléments d'un tableau (reste entier si tout est entier) :

```jslt
{ "total": sum($.n) }
```
```json
{ "n": [1, 2, 3] }
```
```json
{ "total": 6 }
```

`concat(tableau)` joint les éléments en chaîne ; un second argument sert de
séparateur :

```jslt
{ "colle": concat($.parts), "joint": concat($.parts, "-") }
```
```json
{ "parts": ["a", "b", "c"] }
```
```json
{ "colle": "abc", "joint": "a-b-c" }
```

`distinct(source, chemin)` déduplique les valeurs sélectionnées par le chemin
(le second argument est un **chemin compilé**, appliqué à `source`) :

```jslt
{ "uniques": distinct($.vals, $.*) }
```
```json
{ "vals": [1, 2, 2, 3, 3, 3] }
```
```json
{ "uniques": [1, 2, 3] }
```

### Maths : `min`, `max`, `abs`, `floor`, `round`…

Quirks .NET conservés : `floor`/`round`/`min`/`max` renvoient un **flottant**,
`round` fait un **arrondi bancaire** (0.5 → 0, 1.5 → 2), et `min`/`max` sont
**binaires** (deux arguments).

```jslt
{ "min": min($.a, $.b), "max": max($.a, $.b), "abs": abs($.n), "floor": floor($.d) }
```
```json
{ "a": 2, "b": 8, "n": -5, "d": 2.9 }
```
```json
{ "min": 2.0, "max": 8.0, "abs": 5, "floor": 2.0 }
```

Arrondi bancaire :

```jslt
{ "demi": round($.x), "trois_demis": round($.y) }
```
```json
{ "x": 0.5, "y": 1.5 }
```
```json
{ "demi": 0.0, "trois_demis": 2.0 }
```

### Texte : `upper`, `lower`, `trim`, `split`, `startswith`, `stringcontains`…

```jslt
{ "maj": upper($.s), "parts": split($.s, ",") }
```
```json
{ "s": "a,b,c" }
```
```json
{ "maj": "A,B,C", "parts": ["a", "b", "c"] }
```

```jslt
{ "trim": trim($.s), "debut": startswith($.s, " h"), "contient": stringcontains($.s, "ell") }
```
```json
{ "s": " hello " }
```
```json
{ "trim": "hello", "debut": true, "contient": true }
```

### Collections : `limit`, `union`, `select`, `selectmany`

```jslt
{ "deux": limit($.a, 2), "aplati": union($.groups) }
```
```json
{ "a": [1, 2, 3, 4], "groups": [[1, 2], [3, 4], [5]] }
```
```json
{ "deux": [1, 2], "aplati": [1, 2, 3, 4, 5] }
```

`select(source, chemin)` renvoie la **première** valeur sélectionnée ;
`selectmany(source, chemin)` les renvoie **toutes** (chemin compilé) :

```jslt
{ "premier": select($.items, $.*.n), "tous": selectmany($.items, $.*.n) }
```
```json
{ "items": [ { "n": 1 }, { "n": 2 } ] }
```
```json
{ "premier": 1, "tous": [1, 2] }
```

> D'autres fonctions sont portées (trigonométrie, encodage base64 / hash,
> `isnull`, `uuid`, `now`…). Voir la liste complète dans [`CLAUDE.md`](../CLAUDE.md).
> `uuid()` et `now()` sont non déterministes et donc non illustrées ici.

---

## 9. Casts `#type`

Un suffixe `#type` convertit la valeur. Types pris en charge pleinement :
`#integer`, `#decimal`, `#string`, `#boolean`.

```jslt
{ "i": $.s #integer, "d": $.s2 #decimal, "str": $.n #string, "b": $.s3 #boolean }
```
```json
{ "s": "42", "s2": "3.14", "n": 42, "s3": "true" }
```
```json
{ "i": 42, "d": 3.14, "str": "42", "b": true }
```

> Un cast `x #type` est équivalent à `convert(x, "type")` ; c'est d'ailleurs sous
> cette forme qu'il est re-sérialisé par `to_source()`.

---

## 10. Chaînage `->`

`a -> f()` passe `a` comme premier argument à `f` : `$.n -> sum()` équivaut à
`sum($.n)`. Pratique pour lire de gauche à droite.

```jslt
{ "total": $.n -> sum() }
```
```json
{ "n": [1, 2, 3] }
```
```json
{ "total": 6 }
```

---

## 11. `when` / `switch`

`when(expr) { "cas": bloc, ..., "default": bloc }` compare `expr` (`==`) au nom de
chaque cas et renvoie le bloc du premier cas correspondant ; sinon `default` ;
sinon `null`. `switch` est un **alias** de `when`. La comparaison coerce les
types, donc un code numérique matche un nom de cas textuel.

```jslt
{ "statut": when($.code) { "200": "ok", "404": "introuvable", "default": "autre" } }
```
```json
{ "code": 404 }
```
```json
{ "statut": "introuvable" }
```

Sans cas correspondant ni `default`, le résultat est `null` :

```jslt
{ "statut": when($.code) { "200": "ok" } }
```
```json
{ "code": 500 }
```
```json
{ "statut": null }
```

---

## 12. Boucles `$source` / `$where`

Un tableau contenant **un objet** doté de `"$source"` est une **boucle** : l'objet
est produit pour chaque élément de `$source`, et `$` y désigne l'**élément
courant**. `"$where"` filtre les éléments (ne garde que ceux dont l'expression est
vraie).

```jslt
[ { "$source": $.users, "nom": $.name, "majeur": $.age >= 18 } ]
```
```json
{ "users": [ { "name": "A", "age": 30 }, { "name": "B", "age": 15 } ] }
```
```json
[ { "nom": "A", "majeur": true }, { "nom": "B", "majeur": false } ]
```

Avec `$where` pour ne garder que les actifs :

```jslt
[ { "$source": $.users, "$where": $.actif, "nom": $.name } ]
```
```json
{ "users": [ { "name": "A", "actif": true }, { "name": "B", "actif": false } ] }
```
```json
[ { "nom": "A" } ]
```

---

## 13. Filtres JSONPath `?(...)`

`$.items[?(cond)]` ne garde que les éléments vérifiant `cond`. Dans la condition,
`@` désigne l'élément courant et `$` la racine du document. Opérateurs :
comparaisons `== != < <= > >=`, logiques `&` (et) / `|` (ou), appartenance `in`.

```jslt
{ "grands": $.items[?(@.n > 1)] }
```
```json
{ "items": [ { "n": 1 }, { "n": 2 }, { "n": 3 } ] }
```
```json
{ "grands": [ { "n": 2 }, { "n": 3 } ] }
```

Et logique `&` (ici une seule correspondance → la valeur, cf. §4) :

```jslt
{ "r": $.items[?(@.ok == true & @.n > 1)] }
```
```json
{ "items": [ { "n": 1, "ok": true }, { "n": 3, "ok": true } ] }
```
```json
{ "r": { "n": 3, "ok": true } }
```

Appartenance `in` à un littéral ou à un chemin :

```jslt
{ "autorises": $.items[?(@.id in [2, 3])] }
```
```json
{ "items": [ { "id": 1 }, { "id": 2 }, { "id": 3 } ] }
```
```json
{ "autorises": [ { "id": 2 }, { "id": 3 } ] }
```

Comparaison à une valeur de la racine :

```jslt
{ "r": $.items[?(@.n >= $.seuil)] }
```
```json
{ "items": [ { "n": 1 }, { "n": 2 }, { "n": 3 } ], "seuil": 2 }
```
```json
{ "r": [ { "n": 2 }, { "n": 3 } ] }
```

Un filtre alimente couramment une boucle :

```jslt
[ { "$source": $.items[?(@.ok == true)], "v": $.n } ]
```
```json
{ "items": [ { "n": 1, "ok": true }, { "n": 2, "ok": false }, { "n": 3, "ok": true } ] }
```
```json
[ { "v": 1 }, { "v": 3 } ]
```

---

## 14. Fonctions de chemin `length()` / `value()`

À la fin d'un chemin, `length()` donne la taille (tableau, objet ou chaîne ;
`null` pour un scalaire non mesurable) et `value()` renvoie la valeur telle
quelle. Utilisables aussi dans les filtres.

```jslt
{ "taille": $.tags.length(), "valeur": $.v.value() }
```
```json
{ "tags": ["a", "b", "c"], "v": 42 }
```
```json
{ "taille": 3, "valeur": 42 }
```

Dans un filtre :

```jslt
{ "r": $.items[?(@.tags.length() > 1)] }
```
```json
{ "items": [ { "tags": ["x"] }, { "tags": ["y", "z"] } ] }
```
```json
{ "r": { "tags": ["y", "z"] } }
```

---

## 15. Re-sérialisation `to_source()`

`JsltTemplate.to_source()` reconstruit un template **valide et ré-analysable** à
partir de l'AST (analogue du `ToString` .NET). Le résultat est équivalent en
**comportement** (pas forcément identique au caractère près) ; un cast `#type` y
réapparaît sous sa forme `convert(x, "type")`.

```python
from jslt import JsltTemplate

tpl = JsltTemplate.parse('{ "sum": $.a + $.b }')
tpl.to_source()                          # -> '{ "sum": $.a + $.b }'
JsltTemplate.parse(tpl.to_source())      # ré-analysable sans erreur
```

---

## 16. Extensibilité : fonctions et plugins

On peut **ajouter** ses propres fonctions, les **isoler**, les **découvrir**, et
consommer des **plugins tiers** installés — l'équivalent idiomatique Python du
mécanisme de services du .NET.

### Ajouter une fonction

```python
from jslt import jslt_function, JsltTemplate

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
from jslt import FunctionRegistry, default_registry, JsltTemplate

sandbox = FunctionRegistry()                      # vide : aucune fonction intégrée
sandbox.register("triple", lambda ctx, x=None: x * 3)
JsltTemplate.parse('{ "r": triple($.n) }').transform({"n": 7}, functions=sandbox)

# Partir des fonctions intégrées sans muter le registre global :
derive = default_registry.copy()
derive.register("triple", lambda ctx, x=None: x * 3)
```

### Découvrir les fonctions disponibles

```python
from jslt import default_registry

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
from jslt import default_registry

json.dumps(default_registry.catalog())   # prêt à transmettre à un éditeur
# [{"name": "distinct", "description": "...", "signature": "distinct(source, path)",
#   "parameters": [{"name": "source", "type": "Any", "required": false, ...},
#                  {"name": "path", "type": "Any", "is_path": true, ...}],
#   "returns": "list", "path_args": [1]}, ...]
```

### Plugins tiers (entry points)

Un paquet installé expose ses fonctions en déclarant le groupe d'entry points
`jslt.functions`. Côté plugin, dans son `pyproject.toml` :

```toml
[project.entry-points."jslt.functions"]
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

## 17. Débogage (pas à pas)

`JsltTemplate.debug(source)` évalue le template en collectant une **trace
pas-à-pas** : une étape par nœud évalué, avec sa localisation, la source courante et
la valeur produite. (Le moteur étant un interpréteur, le débogage se fait au niveau
du template — il n'y a pas de code généré comme en .NET.)

```python
from jslt import JsltTemplate

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

## 18. Erreurs

Un template syntaxiquement invalide lève `JsltSyntaxError` (avec ligne/colonne) :

```python
from jslt import JsltTemplate, JsltSyntaxError

try:
    JsltTemplate.parse('{ "n": ~ }')
except JsltSyntaxError as e:
    print(e.line, e.column)   # position de l'erreur
```

Une construction reconnue par la grammaire mais **non portée** (ex. opérateur de
filtre `contains`, fonction de chemin `size()`) lève `NotImplementedError` avec un
message explicite — jamais un résultat faux :

```python
from jslt import JsltTemplate

JsltTemplate.parse('{ "r": $.a[?(@.x contains 1)] }')   # -> NotImplementedError
```

---

## 19. Aide-mémoire

| Construction | Syntaxe | Section |
|---|---|---|
| Chemin | `$.a.b`, `$.l[0]`, `$.l[1:3]`, `$.*`, `$..k` | [3](#3-jsonpath--lire-la-source) |
| Variable | `"v:": expr`, `v:`, `v:$.x` | [5](#5-variables) |
| Arithmétique | `+ - * / %` | [6](#6-opérateurs) |
| Comparaison | `== != < <= > >=` | [6](#6-opérateurs) |
| Logique booléenne | `&& \|\| !` | [6](#6-opérateurs) |
| Bit-à-bit / XOR | `& \| ^` | [6](#6-opérateurs) |
| Coalescence | `a ?? b` | [7](#7-coalescence--et-valeurs-manquantes) |
| Fonction | `f(a, b)` | [8](#8-fonctions-intégrées) |
| Cast | `expr #integer` | [9](#9-casts-type) |
| Chaînage | `expr -> f()` | [10](#10-chaînage--) |
| Condition | `when(e) { "c": v, "default": d }` | [11](#11-when--switch) |
| Boucle | `[ { "$source": $.l, "$where": c, ... } ]` | [12](#12-boucles-source--where) |
| Filtre | `$.l[?(@.x > 1 & @.y in [..])]` | [13](#13-filtres-jsonpath-) |
| Fonction de chemin | `$.x.length()`, `$.x.value()` | [14](#14-fonctions-de-chemin-length--value) |

Pour l'architecture interne, les patterns de portage et les écarts volontaires
vis-à-vis du .NET, voir [`CLAUDE.md`](../CLAUDE.md).
