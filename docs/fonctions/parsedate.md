<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `parsedate`

*Français · [English](parsedate.en.md)*

Lit une date texte et la rend en ISO 8601 : détection selon la culture, ou masque explicite (dd/MM/yyyy…), avec un fuseau optionnel

```
parsedate(token, culture, mask, timezone)
```

**Exemples**

*Une date **ISO 8601** se lit sans rien : ni culture, ni masque.*

```jslt
{ "d": parsedate($.t) }
```

```json
{ "t": "2026-11-11T09:30:00Z" }
```

```json
{ "d": "2026-11-11T09:30:00+00:00" }
```

*Sans masque, c'est la **culture** qui décide de l'ordre : mois d'abord en `en-US`, jour d'abord partout ailleurs. Le même texte donne deux dates.*

```jslt
{ "us": parsedate($.t, "en-US"), "gb": parsedate($.t, "en-GB") }
```

```json
{ "t": "03/04/2026" }
```

```json
{ "us": "2026-03-04T00:00:00", "gb": "2026-04-03T00:00:00" }
```

*Un mois **en toutes lettres** exige un masque : la détection automatique ne lit que les formes numériques et l'ISO. `MMMM` prend les noms de la culture.*

```jslt
{ "en": parsedate($.a, "en-US", "MMMM d, yyyy"), "fr": parsedate($.b, "fr-FR", "d MMMM yyyy") }
```

```json
{ "a": "November 11, 2026", "b": "11 novembre 2026" }
```

```json
{ "en": "2026-11-11T00:00:00", "fr": "2026-11-11T00:00:00" }
```

*Abrégés (`MMM`, `ddd`), et heure sur 12 h : `h` **exige** `tt`, le désignateur AM/PM de la culture.*

```jslt
{ "jour": parsedate($.a, "en-GB", "ddd, d MMM yyyy"), "heure": parsedate($.b, "en-US", "MM/dd/yyyy h:mm tt") }
```

```json
{ "a": "Wed, 11 Nov 2026", "b": "11/11/2026 2:05 PM" }
```

```json
{ "jour": "2026-11-11T00:00:00", "heure": "2026-11-11T14:05:00" }
```

*Sans séparateurs, un masque suffit. Et un masque d'**une seule lettre** est un masque standard, résolu selon la culture (`d` = date courte).*

```jslt
{ "compact": parsedate($.a, "", "yyyyMMdd"), "court": parsedate($.b, "en-US", "d") }
```

```json
{ "a": "20261111", "b": "11/11/2026" }
```

```json
{ "compact": "2026-11-11T00:00:00", "court": "2026-11-11T00:00:00" }
```

*Une composante absente du masque vient de l'**époque Unix**, jamais d'aujourd'hui : le même template rend la même chose demain.*

```jslt
{ "heure_seule": parsedate($.t, "", "HH:mm") }
```

```json
{ "t": "11:30" }
```

```json
{ "heure_seule": "1970-01-01T11:30:00" }
```

*Le 4e argument **qualifie** une date sans décalage (on lui donne un fuseau) et **convertit** une date qui en porte déjà un.*

```jslt
{ "qualifie": parsedate($.a, "", "", "Europe/Paris"), "convertit": parsedate($.b, "", "", "UTC") }
```

```json
{ "a": "2026-11-11", "b": "2026-11-11T09:30:00+01:00" }
```

```json
{ "qualifie": "2026-11-11T00:00:00+01:00", "convertit": "2026-11-11T08:30:00+00:00" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel | le texte à lire ; `null` donne `null` |
| `culture` | optionnel | décide de l'ordre jour/mois sans masque, et des noms (mois, jours, AM/PM) avec masque : `en-US`, `en-GB`, `fr-FR`, `de-DE`, `es-ES`, `it-IT`, ou vide pour l'invariante (anglais) |
| `mask` | optionnel | masque explicite (`dd/MM/yyyy`, `MMMM d, yyyy`…), **obligatoire** dès qu'un mois ou un jour est écrit en lettres |
| `timezone` | optionnel | nom IANA (`Europe/Paris`), `UTC`/`Z`, ou décalage fixe (`+02:00`) : qualifie une date naïve, convertit une date qui porte déjà un décalage |

**À savoir**

- **Sans masque, seules les formes numériques et l'ISO 8601 sont reconnues.** `parsedate($.t, "en-US")` sur « November 11, 2026 » lève `date illisible` : un mois ou un jour **en lettres** demande un masque (`MMMM`, `MMM`, `dddd`, `ddd`).
- Le vocabulaire complet des jetons — et ce que chacun lit — est dans [Masques de date](../dates.md#masques-de-date). Il est **commun** avec `format` : ce qui s'écrit se relit.
- Les largeurs sont **strictes** : `dd` exige deux chiffres, `d` en accepte un ou deux. `1/2/26` n'est donc pas conforme à `dd/MM/yyyy`, et lève.
- `ddd` / `dddd` (le nom du jour) sont **lus puis ignorés** : ils servent à ce que le masque colle au texte, pas à décider la date.
- Les noms de mois et de jours, le séparateur de date et le désignateur AM/PM viennent de la **culture** (2e argument) : c'est elle qui dit si `MMMM` lit « November » ou « novembre ». Cultures : vide (invariante, anglais), `en-US`, `en-GB`, `fr-FR`, `de-DE`, `es-ES`, `it-IT`.
- `null` donne `null`. Un texte qui n'est pas une date **lève** plutôt que de rendre une date fausse ou « aujourd'hui » : la faute se voit là où elle est.

**Chapitre** : [Dates et heures](../dates.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
