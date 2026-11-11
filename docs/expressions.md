# Expressions : variables, opérateurs, casts — guide jslt

*Français · [English](expressions.en.md)*

[← Guide jslt](guide.md) · les exemples de cette page sont **exécutés par la
suite de tests** (`tests/test_guide_examples.py`), sous la forme de triplets
*template → entrée → sortie*.

---

## Variables

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

## Opérateurs

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

## Coalescence `??` et valeurs manquantes

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

## Casts `#type`

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

## Chaînage `->`

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

## Paramètres externes (`param`, `params`)

`transform(source)` ne prenait que le document : un template ne pouvait recevoir
« la date de référence » ou « l'identifiant du lot » qu'en les injectant dans la
source, ce qui mélange les **données** à transformer et les **réglages** de
l'exécution.

```python
template.transform(document, parameters={"lot": "A-12", "seuil": 100})
```

`param("nom")` lit un paramètre, `param("nom", repli)` fournit une valeur de
secours, `params()` rend l'objet complet (pratique pour tracer le lot dans la
sortie). Un paramètre **fourni à `null`** reste `null` : le repli ne s'applique
qu'à un paramètre *absent*, sinon on ne pourrait pas passer explicitement « pas
de valeur ».

Les paramètres ne sont **pas** visibles dans les chemins JSONPath : `$.lot` ne
les atteint pas. C'est voulu — un réglage n'est pas une donnée du document, et
les mêler rendrait un template dépendant de la façon dont on l'appelle.

```jslt
{ "lot": param("lot", "aucun"), "reglages": params() }
```

```json
{ "x": 1 }
```

```json
{ "lot": "aucun", "reglages": {} }
```

(Sans paramètres, le repli s'applique et `params()` est vide — c'est ce que
montre l'exemple ci-dessus, exécuté sans `parameters=`.)

Ce qui **n'existe pas** : définir une fonction dans le template (ni lambda, ni
macro, ni récursion) et inclure un autre template. Les deux demandent une
nouvelle syntaxe, donc une modification de la grammaire ANTLR et sa
régénération ; elles ne sont pas contournables par une fonction.

---

[← Guide jslt](guide.md)
