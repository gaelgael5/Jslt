# Dates et heures — guide jslt

*Français · [English](dates.en.md)*

[← Guide jslt](guide.md) · les exemples de cette page sont **exécutés par la
suite de tests** (`tests/test_guide_examples.py`), sous la forme de triplets
*template → entrée → sortie*.

---

Il n'y a pas de type date dans le moteur : une date est une **chaîne ISO 8601**
— celle que rendent `now()`, `parsedate` et les fonctions de calcul, celle que
`format` met en forme. `null` traverse ces fonctions sans erreur ; une valeur
qui n'est pas une date ISO, elle, lève plutôt que de rendre `null` en silence.

**Lire — `parsedate(texte, culture, masque, fuseau)`.** Les trois derniers
arguments sont optionnels, et une chaîne vide vaut « absent » :

| Argument | Vide ou absent | Renseigné |
|---|---|---|
| `culture` | culture invariante : mois d'abord (`m/j/a`) | `fr-FR`, `de-DE`, `en-GB`… lisent `j/m/a` ; `en-US` lit `m/j/a` |
| `masque` | détection : ISO 8601, sinon date numérique selon la culture (séparateurs `/ . -`) avec heure `HH:mm[:ss]` optionnelle | lecture **stricte** selon le masque |
| `fuseau` | la date garde ce qu'elle porte : naïve si l'entrée est naïve, son décalage sinon | **qualifie** une date naïve, **convertit** une date qui porte déjà un décalage |

Un fuseau s'écrit en nom IANA (`Europe/Paris`), en `UTC` / `Z`, ou en décalage
fixe (`+02:00`, `-0500`) ; un nom inconnu lève. Qualifier plutôt que décaler est
ce qu'on attend d'une heure locale : `2026-07-10T08:30:00` en `Europe/Paris`
reste 8 h 30, avec le décalage d'été `+02:00`.

```jslt
{ "auto": parsedate($.a, "fr-FR"), "masque": parsedate($.b, "fr-FR", "dddd d MMMM yyyy"), "paris": parsedate($.c, "", "", "Europe/Paris") }
```
```json
{ "a": "22/10/2026 14:05", "b": "jeudi 22 octobre 2026", "c": "2026-11-10T07:30:00Z" }
```
```json
{ "auto": "2026-10-22T14:05:00", "masque": "2026-10-22T00:00:00", "paris": "2026-11-10T08:30:00+01:00" }
```

**Masques de date.** Le masque reprend le vocabulaire .NET de `format` : ce qui
s'écrit se relit.

| Jeton | Lit | Exemple |
|---|---|---|
| `yyyy` | année sur quatre chiffres | `2026` |
| `yy` | année sur deux chiffres : `00`-`49` → 20xx, `50`-`99` → 19xx | `26` → 2026 |
| `MM` / `M` | mois en chiffres | `10` |
| `MMMM` / `MMM` | mois en lettres, complet ou abrégé, selon la culture | `octobre` / `oct.` |
| `dd` / `d` | jour du mois | `22` |
| `dddd` / `ddd` | nom du jour — lu pour que le masque colle, puis ignoré | `jeudi` |
| `HH` / `H` | heure sur 24 h | `14` |
| `hh` / `h` | heure sur 12 h ; exige `t` ou `tt` | `02` |
| `mm` / `m` | minutes | `05` |
| `ss` / `s` | secondes | `09` |
| `f` à `fffffff` | fraction de seconde, autant de chiffres que de `f` | `250` |
| `F` à `FFFFFFF` | idem, mais les chiffres sont optionnels | |
| `tt` / `t` | désignateur AM/PM de la culture, complet ou première lettre | `PM` / `P` |
| `zzz` / `zz` / `z` | décalage horaire | `+01:00` |
| `K` | `Z`, un décalage, ou rien | `Z` |
| `'…'` `"…"` `\x` | littéral, protégé de l'interprétation | `'T'` |
| `/` | séparateur de date **de la culture** (`.` en `de-DE`) | `/` |

Les largeurs sont **strictes**, comme `ParseExact` en .NET : `dd` exige deux
chiffres, `d` en accepte un ou deux. Un masque d'une **seule lettre** est un
masque standard de `format` (`d D t T f F g G s u o`), résolu selon la culture :
`parsedate($.x, "fr-FR", "d")` lit `22/10/2026`. Une composante absente du
masque vaut celle de l'époque Unix (`1970-01-01`, `00:00:00`) — et non
« aujourd'hui », pour qu'un même template ne change pas de résultat selon le
jour où il tourne. Un texte qui ne respecte pas le masque lève.

**Calculer — `dateadd(date, unité, n)` et `datesub(date, unité, n)`.** Unités :
`second`, `minute`, `hour`, `day`, `week`, `month`, `year` (pluriel et casse
tolérés). `n` est un **entier**, négatif accepté : `datesub(d, u, n)` vaut
exactement `dateadd(d, u, -n)`. `month` et `year` sont calendaires et **bornent**
le jour au dernier jour du mois visé — 31 janvier + 1 mois donne le 28 février,
le 29 en année bissextile. Le décalage horaire de l'entrée est conservé.

**Mesurer — `datediff(début, fin, unité)`.** Compte les unités **entières**
écoulées, avec les mêmes unités, et rend un nombre négatif si `fin` précède
`début`. La troncature va **vers zéro** : 36 heures font 1 jour, 12 heures en
font 0, et -36 heures en font -1. `month` et `year` sont calendaires — un mois
n'est entier que si le jour et l'heure de `fin` ont rattrapé ceux de `début`.
Conséquence à connaître : `datediff` n'inverse pas exactement `dateadd` sur ces
deux unités, puisque `dateadd` borne le jour sur les mois courts (du 31 janvier,
`dateadd` d'un mois donne le 28 février, dont `datediff` compte 0 mois entier).
Comparer une date avec fuseau à une date sans fuseau lève, plutôt que d'en
supposer un.

```jslt
{ "jours": datediff($.a, $.b, "day"), "mois": datediff($.a, $.b, "month"), "retour": datediff($.b, $.a, "day") }
```
```json
{ "a": "2026-11-10T08:30:00", "b": "2026-12-25T00:00:00" }
```
```json
{ "jours": 44, "mois": 1, "retour": -44 }
```

**Extraire — `datepart(date, partie)`.** Parties : `year`, `month`, `day`,
`dayofweek`, `hour`, `minute`, `second`, toujours rendues en nombre.
`dayofweek` suit la convention `DayOfWeek` du .NET : **dimanche = 0**, samedi = 6.

```jslt
{ "dans3mois": dateadd($.d, "month", 3), "veille": datesub($.d, "day", 1), "an": datepart($.d, "year"), "jour": datepart($.d, "dayofweek") }
```
```json
{ "d": "2026-11-10T08:30:00" }
```
```json
{ "dans3mois": "2027-02-10T08:30:00", "veille": "2026-11-09T08:30:00", "an": 2026, "jour": 2 }
```

Le bornage du jour, et le chaînage avec `format` pour l'affichage :

```jslt
{ "borne": dateadd($.d, "month", 1), "lisible": format(dateadd($.d, "month", 1), "d MMMM yyyy", "fr-FR") }
```
```json
{ "d": "2026-01-31T00:00:00" }
```
```json
{ "borne": "2026-02-28T00:00:00", "lisible": "28 février 2026" }
```

---

**Voir aussi** : [écrire une date](texte.md#formatage--format) avec `format`,
et `now()` dans [l'aide-mémoire](guide.md#aide-mémoire).

---

[← Guide jslt](guide.md)
