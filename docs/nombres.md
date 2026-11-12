# Nombres et maths — guide jslt

*Français · [English](nombres.en.md)*

[← Guide jslt](guide.md) · les exemples de cette page sont **exécutés par la
suite de tests** (`tests/test_guide_examples.py`), sous la forme de triplets
*template → entrée → sortie*.

---

Trois conventions à connaître avant de lire la suite : `floor`/`round`/`min`/`max`
renvoient un **flottant**, `round` fait un **arrondi bancaire** (0.5 → 0,
1.5 → 2), et `min`/`max` gardent leur forme **binaire** (deux arguments) en plus
d'accepter un tableau.

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

---

## Lire un nombre écrit en texte : `parsenumber`

Le pendant de `parsedate` : le moteur savait **écrire** un nombre selon une
culture (`format($.v, "N2", "fr-FR")`) sans savoir le relire. Un flux dont les
montants arrivent en texte localisé n'était donc pas traitable.

`parsenumber(texte, culture)` utilise les **mêmes** données de culture que
`format`, donc l'aller-retour est fermé par construction. Les symboles autour du
nombre (`€`, `%`, espaces insécables des milliers) sont ignorés ; un entier reste
un entier. Un texte illisible **lève** : rendre `null` transformerait un montant
corrompu en « pas de montant », et le total calculé ensuite serait faux sans que
rien ne le signale.

```jslt
{
  "fr": parsenumber($.a, "fr-FR"),
  "de": parsenumber($.b, "de-DE"),
  "us": parsenumber($.c, "en-US"),
  "retour": parsenumber(format($.d, "N2", "fr-FR"), "fr-FR")
}
```

```json
{ "a": "1 234,56 €", "b": "1.234,56", "c": "1,234.56", "d": 1234.5 }
```

```json
{ "fr": 1234.56, "de": 1234.56, "us": 1234.56, "retour": 1234.5 }
```

## Précision, bornes et bits

| Fonction | Rôle |
|---|---|
| `round(v, décimales)` | arrondi **bancaire**, à l'entier sans le 2e argument |
| `sign(v)` | `-1`, `0` ou `1` |
| `clamp(v, bas, haut)` | ramène dans l'intervalle ; bornes inversées = erreur |
| `gcd(a, b)` | plus grand commun diviseur |
| `shiftleft(v, bits)` / `shiftright(v, bits)` | décalages de bits |
| `tohex(v, largeur)` / `fromhex(t)` | hexadécimal (`0x` toléré en lecture) |

`round` gardait son arrondi bancaire à l'entier, ce qui obligeait à multiplier
par 100, arrondir, rediviser — avec l'erreur de représentation que ça traîne. Le
second argument fait le travail, **en gardant l'arrondi bancaire** : `round(0.25,
1)` donne `0.2`, pas `0.3`.

Les décalages de bits sont des **fonctions** et non des opérateurs : ajouter
`<<` et `>>` à la grammaire imposerait de régénérer le parser ANTLR, alors que
`&`, `|` et `^` existent déjà comme opérateurs. `gcd` et les décalages exigent
des **entiers** et lèvent sur un décimal, plutôt que de tronquer en silence.

`tohex` écrit le signe devant les chiffres (`-ff`) : un entier JSON n'a pas de
largeur, donc pas de représentation signée naturelle en complément à deux.

```jslt
{
  "arrondi": round($.v, 2),
  "borne": clamp($.v, 0, 10),
  "signe": sign($.v),
  "hex": tohex($.n, 4),
  "lu": fromhex($.h)
}
```

```json
{ "v": 12.345, "n": 255, "h": "0x1F" }
```

```json
{ "arrondi": 12.35, "borne": 10, "signe": 1, "hex": "00ff", "lu": 31 }
```

---

## Arrondis dirigés et précision

`floor` existait **sans** `ceil` : l'asymétrie la plus visible du portage, qui
obligeait à écrire `0 - floor(0 - x)`. `ceil` est là, et les trois arrondis
dirigés acceptent une précision.

| Appel | Résultat |
|---|---|
| `ceil(2.1)` | `3.0` |
| `ceil(1.2345, 2)` | `1.24` |
| `floor(1.2345, 2)` | `1.23` |
| `truncate(-1.2345, 2)` | `-1.23` (vers zéro) |
| `floor(-1.2345, 2)` | `-1.24` (vers le bas) |

`truncate` coupe vers zéro, `floor` descend : sur un négatif, les deux
diffèrent, et c'est tout l'intérêt d'avoir les deux. `round` reste l'arrondi
**bancaire** (cf. ci-dessus).

### Arrondi commercial, au multiple, aux chiffres significatifs

`round` est l'arrondi **bancaire** : les demis vont vers le pair, donc
`round(0.125, 2)` rend `0.12` là où une facture attend `0.13`. Trois fonctions
couvrent ce que ce choix laisse dehors.

| Fonction | Rôle |
|---|---|
| `roundhalfup(v, décimales)` | arrondi commercial : les demis **s'éloignent de zéro** (`-0.5` → `-1`) |
| `roundto(v, pas)` | arrondi au multiple le plus proche : le pas de 0,05 d'une caisse, le quart d'heure |
| `toprecision(v, chiffres)` | arrondi à un nombre de chiffres **significatifs**, pas de décimales |

Les trois lisent le nombre tel qu'il est **écrit** : `2.675` se stocke en
`2.67499999…`, et un arrondi qui travaillerait sur cette valeur rendrait `2.67`.
C'est l'arrondi « faux » que tout le monde rencontre une fois, et c'est aussi ce
que rend le contournement `round($.n * 20) / 20`. Un pas nul ou négatif **lève**,
plutôt que de rendre une valeur qui n'a été arrondie à rien ; `toprecision`
exige au moins un chiffre. Comme `round`, `floor` et `ceil`, les trois rendent un
**décimal**.

```jslt
{ "facture": roundhalfup($.n, 2), "caisse": roundto($.n, 0.05), "mesure": toprecision($.n, 3), "bancaire": round($.n, 2) }
```
```json
{ "n": 2.675 }
```
```json
{ "facture": 2.68, "caisse": 2.7, "mesure": 2.68, "bancaire": 2.67 }
```

`toprecision` sert là où l'ordre de grandeur **varie** : `round($.n, 2)` fixe le
rang de la virgule, ce qui n'a pas de sens sur une colonne où voisinent
`0.00241` et `24100`.

## Logarithme, bases et valeurs non finies

| Fonction | Rôle |
|---|---|
| `log(v, base)` | logarithme dans une base libre (`logarithm` est fixé à e, ses variantes à 10 et 2) |
| `tobase(v, base, largeur)` / `frombase(t, base)` | écriture dans une base de 2 à 36 |
| `isfinite(v)` / `isnan(v)` | la valeur est-elle un nombre exploitable ? |

`log(1000, 10)` rend exactement `3.0` : les bases 10 et 2 passent par leur
fonction dédiée, parce que diviser deux logarithmes rendrait
`2.9999999999999996` — et ce nombre ressortirait tel quel dans le JSON produit.

`isfinite` sert là où JSON est muet : un calcul **peut** produire l'infini (le
débordement d'un produit) alors que la notation JSON ne sait pas l'écrire. Sans
test, la valeur se propage et ressort en `Infinity`, que la plupart des lecteurs
refusent.

`tohex` / `fromhex` restent : ce sont les cas particuliers qu'on écrit le plus
souvent, et ils concordent avec `tobase(v, 16)`.

```jslt
{
  "haut": ceil($.v, 2),
  "bits": tobase($.n, 2, 8),
  "lu": frombase($.t, 36),
  "exploitable": isfinite($.v * $.v)
}
```

```json
{ "v": 1.2345, "n": 5, "t": "73" }
```

```json
{ "haut": 1.24, "bits": "00000101", "lu": 255, "exploitable": true }
```

---

[← Guide jslt](guide.md)
