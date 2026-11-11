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
(`"\\d+"`). La syntaxe .NET des groupes nommés `(?<nom>…)` est acceptée.

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

`format(valeur, masque, culture)` reprend les masques .NET : nombres (`N2`,
`C`, `P1`, `D5`, `#,##0.00`…) et dates — une chaîne ISO 8601 est une date —
(`d`, `D`, `dd/MM/yyyy`, `dddd d MMMM yyyy`…). Cultures : invariante (vide),
`en-US`, `en-GB`, `fr-FR`, `de-DE`, `es-ES`, `it-IT`. Un masque hors de ce
sous-ensemble lève une erreur plutôt qu'un texte approximatif.

Le décalage horaire s'écrit aussi (`zzz`, `zz`, `z`, et `K` qui rend `Z` pour
UTC et rien pour une date sans fuseau), de sorte que `parsedate(…, fuseau)` et
`format` font l'aller-retour. Comme en .NET, un spécificateur **seul** (`"z"`,
`"K"`) est lu comme un masque standard, et refusé : il faut l'écrire dans un
masque plus long (`"HH:mmK"`).

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

**Bornes tolérantes.** `Substring` en .NET jette dès que les bornes sortent de la
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

**`regexreplace` suit la syntaxe .NET** pour le remplacement : `$1` pour un
groupe numéroté, `${nom}` pour un groupe nommé, `$&` pour la correspondance
entière, `$$` pour un `$` littéral. C'est traduit vers le dialecte Python, donc
un remplacement écrit pour le .NET se comporte pareil.

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
au .NET, et c'est un piège : `split($.t, ", ")` coupe sur la virgule et laisse
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
