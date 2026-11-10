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

**Voir aussi** : [Dates et heures](dates.md) pour lire une date (`parsedate`)
et la calculer.

---

[← Guide jslt](guide.md)
