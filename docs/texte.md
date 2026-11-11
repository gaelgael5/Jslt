# Texte, expressions régulières et formatage — guide jslt

*Français · [English](texte.en.md)*

[← Guide jslt](guide.md) · les exemples de cette page sont **exécutés par la
suite de tests** (`tests/test_guide_examples.py`), sous la forme de triplets
*template → entrée → sortie*.

---

## Texte : `upper`, `lower`, `trim`, `split`, `startswith`, `stringcontains`…

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

---

## Expressions régulières : `regexismatch`, `regexmatches`

`regexismatch(texte, motif)` dit si le texte contient une correspondance ;
`regexmatches(texte, motif)` rend la liste des correspondances complètes. Un
nombre ou un booléen est converti en texte avant la recherche ; `null`, un objet
ou un tableau donnent `null`. Dans une chaîne jslt, l'antislash se double
(`"\\d+"`). Les groupes **nommés** s'écrivent `(?<nom>…)` ou `(?P<nom>…)` : les
deux formes sont acceptées.

```jslt
{ "valide": regexismatch($.mail, "^[\\w.]+@[\\w.]+\\.[a-z]+$"), "nombres": regexmatches($.s, "\\d+") }
```
```json
{ "mail": "bob@ex.fr", "s": "lot 12, ref 345" }
```
```json
{ "valide": true, "nombres": ["12", "345"] }
```

---

## Unicode : `normalize`

`normalize` compose les caractères Unicode (forme C).

---

## Formatage : `format`

`format(valeur, masque, culture)` écrit un **nombre** ou une **date** (une chaîne
ISO 8601 **est** une date) selon un masque. Un masque hors du vocabulaire
ci-dessous **lève** plutôt que de rendre un texte approximatif.

**Masques de nombre standards** : une lettre, suivie d'une précision optionnelle
(`N2`, `F0`, `D5`). Colonne de droite : `1234.5` en `fr-FR`.

| Masque | Rend | Exemple |
|---|---|---|
| `N` | nombre **groupé** par milliers, 2 décimales par défaut | `1 234,50` |
| `F` | nombre **non groupé** | `1234,50` |
| `C` | montant, avec le symbole monétaire de la culture | `1 234,50 €` |
| `P` | pourcentage — la valeur est multipliée par 100 | `123 450,00 %` |
| `D` | entier complété de zéros à gauche (`D5` = cinq chiffres) | `00042` (de `42`) |
| `X` / `x` | entier en hexadécimal, majuscule ou minuscule | `002A` (de `42`, `X4`) |
| `E` / `e` | notation scientifique, 6 décimales par défaut | `1,234500E+003` |
| `G` | la représentation la plus courte qui fait l'aller-retour | `1234,5` |

**Masques de nombre personnalisés** : un assemblage de ces caractères.

| Caractère | Rôle |
|---|---|
| `0` | chiffre **toujours** écrit (un zéro s'il n'y en a pas) |
| `#` | chiffre écrit seulement s'il existe |
| `.` | séparateur décimal **de la culture** |
| `,` | séparateur de milliers **de la culture** |
| `%` | multiplie par 100 et écrit le signe |
| `'…'` `"…"` `\x` | littéral, en tête ou en fin de masque |

D'où `#,##0.00` → `1 234,50` en `fr-FR`, et `1,234.50` en `en-US` : c'est la
culture qui décide des séparateurs, pas le masque.

**Masques de date.** Le vocabulaire des jetons (`yyyy`, `MM`, `MMMM`, `dd`,
`dddd`, `HH`, `mm`, `ss`, `tt`, `zzz`, `K`, littéraux…) est **commun** à la
lecture : son tableau est dans [Dates et heures](dates.md#masques-de-date). S'y
ajoutent les masques **standards** d'une lettre, résolus selon la culture :

| Masque | Rend |
|---|---|
| `d` / `D` | date courte / date longue |
| `t` / `T` | heure courte / heure longue |
| `f` / `F` | date longue + heure courte / + heure longue |
| `g` / `G` | date courte + heure courte / + heure longue |
| `s` | ISO 8601 triable (`2026-10-22T14:05:00`) |
| `u` | ISO 8601 universel (`2026-10-22 14:05:00Z`) |
| `o` / `O` | aller-retour complet, à la fraction de seconde près |

**Cultures** : invariante (chaîne vide, ou `invariant`), `en-US`, `en-GB`,
`fr-FR`, `de-DE`, `es-ES`, `it-IT`. Elles fixent les séparateurs décimal et de
milliers, le symbole monétaire, les noms de jours et de mois, le désignateur
AM/PM et le séparateur de date (`/` s'écrit `.` en `de-DE`). Une culture inconnue
lève, avec la liste de celles qui existent.

Le décalage horaire s'écrit aussi (`zzz`, `zz`, `z`, et `K` qui rend `Z` pour
UTC et rien pour une date sans fuseau), de sorte que `parsedate(…, fuseau)` et
`format` font l'aller-retour. Un spécificateur **seul** (`"z"`, `"K"`) est lu
comme un masque standard d'une lettre — et il n'en existe pas pour ces deux-là,
donc il est refusé : il faut l'écrire dans un masque plus long (`"HH:mmK"`).

```jslt
{ "prix": format($.p, "#,##0.00"), "jour": format($.d, "dddd d MMMM yyyy", "fr-FR"), "code": format($.n, "D5") }
```
```json
{ "p": 1234.5, "d": "2026-10-22T14:05:00", "n": 42 }
```
```json
{ "prix": "1,234.50", "jour": "jeudi 22 octobre 2026", "code": "00042" }
```

---

## Extraire et remplacer : `substring`, `replace`, `regexreplace`

Le moteur savait **mesurer** une chaîne (`indexof`, `lastindexof`,
`stringlenght`) sans pouvoir en découper un morceau : les bornes se calculaient
sans que rien ne les consomme.

| Fonction | Rôle |
|---|---|
| `substring(t, début, longueur)` | morceau de chaîne ; `début` négatif = depuis la fin, `longueur` absente = jusqu'au bout |
| `replace(t, cherché, remplacement)` | toutes les occurrences, texte brut |
| `regexreplace(t, motif, remplacement)` | par expression régulière, avec `$1`, `${nom}`, `$&` |
| `trimstart(t, caractères)` / `trimend(t, caractères)` | rognage dirigé |
| `repeat(t, n)` | répétition (`n` ≤ 0 : chaîne vide) |
| `titlecase(t)` | majuscule initiale de chaque mot, **le reste intact** |

**Bornes tolérantes.** `substring` ne lève **pas** dès que les bornes sortent de la
chaîne ; ici un début hors bornes rend une chaîne vide et une longueur trop
grande s'arrête au bout. Un template transforme des données qu'il ne choisit
pas : tomber sur un champ plus court que prévu ne doit pas faire échouer toute la
transformation. Une longueur **négative** lève, elle : c'est une faute
d'écriture, pas une donnée surprenante.

**`titlecase` ne rabaisse rien.** Un `str.title()` classique transformerait un
« McDonald » correct en « Mcdonald ». Sur des noms venus de données réelles,
c'est une dégradation : seule la première lettre de chaque mot est touchée.

```jslt
{
  "code": substring($.adresse, -5, 5),
  "rue": substring($.adresse, 0, 16),
  "sans_tiret": replace($.tel, "-", ""),
  "nom": titlecase($.nom)
}
```

```json
{ "adresse": "12 rue des Lilas 75011", "tel": "01-02-03-04-05", "nom": "ana McDonald" }
```

```json
{
  "code": "75011",
  "rue": "12 rue des Lilas",
  "sans_tiret": "0102030405",
  "nom": "Ana McDonald"
}
```

**Le remplacement de `regexreplace` s'écrit avec `$`** : `$1` pour un
groupe numéroté, `${nom}` pour un groupe nommé, `$&` pour la correspondance
entière, `$$` pour un `$` littéral. C'est traduit vers le dialecte Python, donc
la même écriture vaut des deux côtés.

Attention à la convention : comme `regexismatch` et `regexmatches`,
`regexreplace` **convertit un scalaire en texte** (`42` devient `"42"`), là où
`replace` rendrait `false`. Chercher un motif dans un nombre a un sens ; le
mettre en majuscules non.

```jslt
{ "iso": regexreplace($.d, "(\\d{2})/(\\d{2})/(\\d{4})", "$3-$2-$1") }
```

```json
{ "d": "24/12/2026" }
```

```json
{ "iso": "2026-12-24" }
```

## Comparer sans la casse ni les accents : `foldtext`, `deaccent`

`normalize` accepte désormais une **forme** (`C` par défaut, `D`, `KC`, `KD`).
`deaccent` retire les diacritiques sans toucher à la casse. `foldtext` rend une
**clé de comparaison** : minuscules *et* sans accents par défaut, ou seulement
`case`, ou seulement `accents`.

Pourquoi une clé plutôt qu'un opérateur « insensible à la casse » ? Parce qu'un
second `==` aurait dédoublé la sémantique du premier, et parce que la même clé
sert aussi à **trier** (cf. [`sort`](collections.md#trier-et-ordonner-sort-reverse-first-last)).

```jslt
{
  "meme": foldtext($.a) == foldtext($.b),
  "sans_accent": deaccent($.a),
  "clef": foldtext($.a)
}
```

```json
{ "a": "CRÈME", "b": "creme" }
```

```json
{ "meme": true, "sans_accent": "CREME", "clef": "creme" }
```

---

## Découper finement : `splitstring`, `splitregex`

**`split` ne retient que le premier caractère du séparateur.** C'est la fidélité
historique, et c'est un piège : `split($.t, ", ")` coupe sur la virgule et laisse
les espaces, silencieusement. D'où deux fonctions plutôt qu'un changement de
`split`, qui casserait les templates portés :

- `splitstring(t, séparateur, limite)` coupe sur le séparateur **entier**, au
  plus `limite` fois ;
- `splitregex(t, motif, limite)` coupe sur un motif, pour les séparateurs à
  géométrie variable (`"a ; b;c"`).

```jslt
{
  "piege": split($.t, ", "),
  "correct": splitstring($.t, ", "),
  "variable": splitregex($.v, "\\s*;\\s*")
}
```

```json
{ "t": "a, b, c", "v": "a ; b;c" }
```

```json
{ "piege": ["a", " b", " c"], "correct": ["a", "b", "c"], "variable": ["a", "b", "c"] }
```

## Raccourcir, retourner, identifier

| Fonction | Rôle |
|---|---|
| `shorten(t, longueur, suffixe)` | raccourcit avec une ellipse, **suffixe compris** dans la longueur |
| `reverse(t)` | retourne un texte (ou un tableau) |
| `slugify(t, séparateur)` | identifiant d'URL : sans accent, en minuscules, mots joints |

Le nom n'est pas `truncate` : il est déjà pris par la troncature **numérique**.
Le suffixe compte dans la longueur demandée, sinon « 8 caractères maximum » en
rendrait 9 et déborderait la colonne qu'on voulait tenir. Et quand la coupe
tombe au milieu d'un mot, `shorten` remonte au dernier espace — « Paris L… »
donne à lire un mot qui n'existe pas ; sans espace dans la fenêtre (un
identifiant, un mot très long), il coupe net plutôt que de tout perdre.

`reverse` accepte maintenant une chaîne (il rendait `null`), et retourne par
**graphème** : sur un « é » écrit en forme décomposée, inverser les points de
code collerait l'accent sur la lettre voisine.

```jslt
{
  "court": shorten($.t, 12),
  "slug": slugify($.t),
  "envers": reverse($.mot)
}
```

```json
{ "t": "Crème Brûlée à Paris", "mot": "été" }
```

```json
{ "court": "Crème…", "slug": "creme-brulee-a-paris", "envers": "été" }
```

## Rapprocher deux écritures : `levenshtein`, `similarity`

`==` répond « identiques ou non », `foldtext` rapproche la casse et les accents ;
reste la faute de frappe. `levenshtein(a, b)` compte les caractères à insérer,
supprimer ou remplacer ; `similarity(a, b)` ramène ce compte entre 0 et 1, plus
facile à seuiller. Deux chaînes vides valent 1 : elles sont identiques, et rendre
« indéfini » obligerait chaque appelant à traiter ce cas.

Le coût est en O(n·m) : c'est l'outil des libellés, pas des documents.

```jslt
{
  "distance": levenshtein($.a, $.b),
  "proche": similarity(foldtext($.a), foldtext($.b)) > 0.8
}
```

```json
{ "a": "Crème brulee", "b": "creme brûlée" }
```

```json
{ "distance": 4, "proche": true }
```

---

**Voir aussi** : [Dates et heures](dates.md) pour lire une date (`parsedate`)
et la calculer.

---

[← Guide jslt](guide.md)
