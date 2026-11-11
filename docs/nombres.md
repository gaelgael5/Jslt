# Nombres et maths — guide jslt

*Français · [English](nombres.en.md)*

[← Guide jslt](guide.md) · les exemples de cette page sont **exécutés par la
suite de tests** (`tests/test_guide_examples.py`), sous la forme de triplets
*template → entrée → sortie*.

---

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

[← Guide jslt](guide.md)
