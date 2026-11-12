"""Un exemple exécuté par fonction, inlined dans sa page de référence.

Pourquoi ici et pas dans les chapitres : un exemple de chapitre enseigne un
*usage* et mêle souvent trois fonctions (`selectmany(sort(…), …)`) ; la page de
référence, elle, doit montrer **une** fonction, au plus court. Les deux ont leur
place, et ce fichier porte la seconde.

Pourquoi des données et pas du texte écrit dans les pages : chaque exemple est
rejoué par la suite du guide (`tests/_docs.py` balaie aussi `docs/fonctions/`),
donc par les **deux** moteurs — interprété et compilé. Un exemple faux fait
rougir la suite au lieu d'égarer le lecteur.

Forme d'un exemple :

    {"template": …, "source": …, "output": …}      exécuté (triplet du guide)
    {"template": …, "source": …, "render": …}      sortie texte : `render()`,
                                                   donc montré sans être rejoué

Les clés des documents sont **courtes et neutres** : le même exemple sert les
deux langues, le code n'ayant pas à être traduit.
"""

from __future__ import annotations

#: Rôle de chaque argument, par fonction : {nom: (français, anglais)}.
#: « optionnel » ne dit pas ce qu'on met dedans ; ces lignes-là, si. Rempli là où
#: l'argument ne se devine pas — un `token` d'`abs` se passe de commentaire.
PARAMS: dict[str, dict[str, tuple[str, str]]] = {
    "parsedate": {
        "token": ("le texte à lire ; `null` donne `null`", "the text to read; `null` gives `null`"),
        "culture": (
            ("décide de l'ordre jour/mois sans masque, et des noms (mois, jours, AM/PM) avec "
            "masque : `en-US`, `en-GB`, `fr-FR`, `de-DE`, `es-ES`, `it-IT`, ou vide pour "
            "l'invariante (anglais)"),
            ("decides the day/month order without a mask, and the names (months, days, AM/PM) "
            "with one: `en-US`, `en-GB`, `fr-FR`, `de-DE`, `es-ES`, `it-IT`, or empty for "
            "the invariant one (English)"),
        ),
        "mask": (
            ("masque explicite (`dd/MM/yyyy`, `MMMM d, yyyy`…), **obligatoire** dès qu'un "
            "mois ou un jour est écrit en lettres"),
            ("explicit mask (`dd/MM/yyyy`, `MMMM d, yyyy`…), **required** as soon as a month "
            "or a day is spelled out"),
        ),
        "timezone": (
            ("nom IANA (`Europe/Paris`), `UTC`/`Z`, ou décalage fixe (`+02:00`) : qualifie "
            "une date naïve, convertit une date qui porte déjà un décalage"),
            ("IANA name (`Europe/Paris`), `UTC`/`Z`, or a fixed offset (`+02:00`): qualifies "
            "a naive date, converts one that already carries an offset"),
        ),
    },
    "format": {
        "token": ("le nombre, ou la date ISO 8601, à écrire", "the number, or ISO 8601 date, to write"),
        "mask": (
            ("masque de nombre (`N2`, `#,##0.00`…) ou de date (`dd/MM/yyyy`, "
            "`dddd d MMMM yyyy`, ou une lettre standard)"),
            ("number mask (`N2`, `#,##0.00`…) or date mask (`dd/MM/yyyy`, "
            "`dddd d MMMM yyyy`, or a standard letter)"),
        ),
        "culture": (
            ("séparateurs, symbole monétaire, noms de jours et de mois : `en-US`, `en-GB`, "
            "`fr-FR`, `de-DE`, `es-ES`, `it-IT`, ou vide pour l'invariante"),
            ("separators, currency symbol, day and month names: `en-US`, `en-GB`, `fr-FR`, "
            "`de-DE`, `es-ES`, `it-IT`, or empty for the invariant one"),
        ),
    },
    "dateadd": {
        "token": ("la date ISO 8601 de départ", "the ISO 8601 date to start from"),
        "unit": (
            "`second`, `minute`, `hour`, `day`, `week`, `month` ou `year` (pluriel toléré)",
            "`second`, `minute`, `hour`, `day`, `week`, `month` or `year` (plural tolerated)",
        ),
        "amount": ("nombre entier, négatif pour retrancher", "whole number, negative to subtract"),
    },
    "datesub": {
        "token": ("la date ISO 8601 de départ", "the ISO 8601 date to start from"),
        "unit": (
            "`second`, `minute`, `hour`, `day`, `week`, `month` ou `year` (pluriel toléré)",
            "`second`, `minute`, `hour`, `day`, `week`, `month` or `year` (plural tolerated)",
        ),
        "amount": ("nombre entier", "whole number"),
    },
    "datediff": {
        "start": ("date ISO 8601 de début", "ISO 8601 start date"),
        "end": (
            "date ISO 8601 de fin ; avant le début, le résultat est négatif",
            "ISO 8601 end date; before the start, the result is negative",
        ),
        "unit": (
            "`second`, `minute`, `hour`, `day`, `week`, `month` ou `year`",
            "`second`, `minute`, `hour`, `day`, `week`, `month` or `year`",
        ),
    },
    "datepart": {
        "token": ("la date ISO 8601 à décomposer", "the ISO 8601 date to break down"),
        "part": (
            ("`year`, `quarter`, `month`, `day`, `dayofweek`, `dayofyear`, `week`, `hour`, "
            "`minute` ou `second`"),
            ("`year`, `quarter`, `month`, `day`, `dayofweek`, `dayofyear`, `week`, `hour`, "
            "`minute` or `second`"),
        ),
    },
    "datestartof": {
        "token": (
            "la date ISO 8601 à ramener au début de sa période",
            "the ISO 8601 date to bring back to the start of its period",
        ),
        "period": (
            "`year`, `quarter`, `month`, `week` (lundi), `day`, `hour` ou `minute`",
            "`year`, `quarter`, `month`, `week` (Monday), `day`, `hour` or `minute`",
        ),
    },
    "dateendof": {
        "token": (
            "la date ISO 8601 à porter à la fin de sa période",
            "the ISO 8601 date to carry to the end of its period",
        ),
        "period": (
            "`year`, `quarter`, `month`, `week`, `day`, `hour` ou `minute`",
            "`year`, `quarter`, `month`, `week`, `day`, `hour` or `minute`",
        ),
    },
    "datezone": {
        "token": ("la date ISO 8601", "the ISO 8601 date"),
        "zone": (
            "nom IANA (`Europe/Paris`), `UTC`/`Z`, ou décalage fixe (`+02:00`)",
            "IANA name (`Europe/Paris`), `UTC`/`Z`, or a fixed offset (`+02:00`)",
        ),
    },
    "sort": {
        "source": ("le tableau à trier", "the array to sort"),
        "key": (
            ("expression évaluée **par élément** (`$.prix`), un tableau pour trier sur "
            "plusieurs critères, ou rien pour trier les éléments eux-mêmes"),
            ("expression evaluated **per element** (`$.price`), an array to sort on several "
            "criteria, or nothing to sort the elements themselves"),
        ),
        "descending": (
            "`true` pour l'ordre inverse, ou un **tableau de booléens** : un sens par clef",
            "`true` for the reverse order, or an **array of booleans**: one direction per key",
        ),
    },
    "groupby": {
        "source": ("le tableau à regrouper", "the array to group"),
        "key": (
            "expression évaluée **par élément** ; un tableau pour une clef composite",
            "expression evaluated **per element**; an array for a composite key",
        ),
        "nested": (
            "`true` pour imbriquer un niveau d'objet par clef",
            "`true` to nest one object level per key",
        ),
    },
    "sumby": {
        "source": ("le tableau à agréger", "the array to aggregate"),
        "key": (
            "expression de la clef de groupe, évaluée par élément",
            "the group key expression, evaluated per element",
        ),
        "value": (
            "expression de la valeur à sommer ; omise, c'est l'élément",
            "the expression of the value to sum; omitted, it is the element",
        ),
    },
    "avgby": {
        "source": ("le tableau à agréger", "the array to aggregate"),
        "key": (
            "expression de la clef de groupe, évaluée par élément",
            "the group key expression, evaluated per element",
        ),
        "value": (
            "expression de la valeur à moyenner ; omise, c'est l'élément",
            "the expression of the value to average; omitted, it is the element",
        ),
    },
    "ifelse": {
        "condition": (
            ("l'expression à tester ; lue comme celle de `filter` (`null`, `0`, `\"\"`, vide "
            "= faux), pas comme une assertion"),
            ("the expression to test; read like `filter`'s (`null`, `0`, `\"\"`, empty = "
            "false), not like an assertion"),
        ),
        "when_true": (
            "valeur rendue si la condition est vraie ; **non évaluée** sinon",
            "value returned when the condition is true; **not evaluated** otherwise",
        ),
        "when_false": (
            "valeur rendue sinon ; absente, le résultat est `null`",
            "value returned otherwise; absent, the result is `null`",
        ),
    },
    "get": {
        "token": (
            "l'objet ou le tableau à lire ; autre chose rend `null`",
            "the object or array to read; anything else gives `null`",
        ),
        "key": (
            ("la clef, **calculée** : nom pour un objet, indice pour un tableau "
            "(négatif depuis la fin)"),
            ("the key, **computed**: a name for an object, an index for an array "
            "(negative from the end)"),
        ),
    },
    "getpath": {
        "token": (
            "l'objet ou le tableau de départ ; autre chose rend `null`",
            "the starting object or array; anything else gives `null`",
        ),
        "path": (
            ("le chemin pointé, **calculable** (`\"client.ville\"`, `\"lignes.0.ref\"`) ; "
            "mêmes étapes que `setpath`"),
            ("the dotted path, **computable** (`\"client.ville\"`, `\"lignes.0.ref\"`); same "
            "steps as `setpath`"),
        ),
        "separator": (
            "séparateur des étapes, `.` par défaut ; vide, il lève",
            "step separator, `.` by default; empty, it raises",
        ),
    },
    "roundhalfup": {
        "digits": (
            ("nombre de décimales ; absent, arrondi à l'entier ; négatif, aux dizaines "
            "(`-2` = à la centaine)"),
            ("number of decimals; absent, rounds to the integer; negative, to tens "
            "(`-2` = to the hundred)"),
        ),
    },
    "roundto": {
        "step": (
            ("le pas d'arrondi, strictement positif (`0.05`, `15`, `0.25`) ; nul ou "
            "négatif, il lève"),
            ("the rounding step, strictly positive (`0.05`, `15`, `0.25`); zero or "
            "negative, it raises"),
        ),
    },
    "toprecision": {
        "digits": (
            "nombre de chiffres **significatifs**, au moins 1 (et non un nombre de décimales)",
            "number of **significant** digits, at least 1 (not a number of decimals)",
        ),
    },
}

#: Ce qu'un exemple ne montre pas, par fonction : couples (français, anglais).
#: Les refus, les valeurs par défaut et les pièges — c'est ce qui fait la
#: différence entre une fiche signalétique et une aide.
NOTES: dict[str, list[tuple[str, str]]] = {
    "distinct": [
        (
            ("Le chemin s'applique au **tableau entier** (`$.*.v`), pas à chaque élément — "
             "convention inverse de `sort` et `distinctby`, dont la clef est évaluée par "
             "élément."),
            ("The path applies to the **whole array** (`$.*.v`), not to each element — the "
             "opposite convention to `sort` and `distinctby`, whose key is evaluated per "
             "element."),
        ),
        (
            "Pour dédupliquer des **objets** sur une clef, c'est `distinctby`.",
            "To deduplicate **objects** on a key, use `distinctby`.",
        ),
    ],
    "select": [
        (
            ("Le 2e argument est un **argument-chemin** : il n'est pas évalué comme une "
             "expression, il est appliqué à `source`. Il s'écrit aussi en chaîne "
             "(`\"$.client.nom\"`)."),
            ("The 2nd argument is a **path argument**: it is not evaluated as an expression, "
             "it is applied to `source`. It can also be written as a string "
             "(`\"$.client.nom\"`)."),
        ),
        (
            "Plusieurs valeurs trouvées : c'est la **première**. Aucune : `null`.",
            "Several values found: the **first** one. None: `null`.",
        ),
    ],
    "selectmany": [
        (
            ("Argument-chemin appliqué à `source`, comme `select`, mais il rend **toutes** "
             "les valeurs sélectionnées, dans l'ordre du document."),
            ("A path argument applied to `source`, like `select`, but it returns **all** the "
             "selected values, in document order."),
        ),
    ],
    "selectany": [
        (
            ("Compte les **nœuds** sélectionnés, pas leur vérité : une valeur `0` ou `\"\"` "
             "trouvée rend `true`."),
            ("Counts the **nodes** selected, not their truth: a `0` or `\"\"` value found "
             "returns `true`."),
        ),
    ],
    "substring": [
        (
            ("Des bornes trop larges ne **lèvent pas** : un début hors du texte rend une "
             "chaîne vide, une longueur trop grande s'arrête à la fin. Un template "
             "transforme des données qu'il ne choisit pas."),
            ("Out-of-range bounds do **not raise**: a start beyond the text gives an empty "
             "string, an over-long length stops at the end. A template transforms data it "
             "does not choose."),
        ),
        (
            "Une longueur **négative** lève, elle : c'est une faute d'écriture.",
            "A **negative** length does raise: that is an authoring mistake.",
        ),
    ],
    "split": [
        (
            ("Seul le **premier caractère** du séparateur est retenu : `split($.t, \", \")` "
             "coupe sur la virgule et laisse les espaces. Pour un séparateur entier, "
             "`splitstring`."),
            ("Only the **first character** of the separator is kept: `split($.t, \", \")` cuts "
             "on the comma and leaves the spaces. For a whole separator, use `splitstring`."),
        ),
    ],
    "splitstring": [
        (
            ("`limit` est le nombre de **coupes**, pas de morceaux : avec `1`, on obtient "
             "deux éléments et le reste du texte est gardé entier."),
            ("`limit` is the number of **cuts**, not of pieces: with `1` you get two "
             "elements and the rest of the text is kept whole."),
        ),
    ],
    "shorten": [
        (
            ("La longueur **comprend le suffixe** (`…` par défaut), et la coupe remonte au "
             "dernier espace : on ne coupe pas un mot en deux."),
            ("The length **includes the suffix** (`…` by default), and the cut backs up to "
             "the last space: a word is not cut in half."),
        ),
    ],
    "replace": [
        (
            ("Remplace **toutes** les occurrences, littéralement : aucun caractère n'a de "
             "sens particulier. Pour un motif, `regexreplace`."),
            ("Replaces **every** occurrence, literally: no character has a special meaning. "
             "For a pattern, use `regexreplace`."),
        ),
    ],
    "regexreplace": [
        (
            ("Le remplacement s'écrit avec `$` : `$1` (groupe numéroté), `${nom}` (groupe "
             "nommé), `$&` (toute la correspondance), `$$` (un `$` littéral)."),
            ("The replacement is written with `$`: `$1` (numbered group), `${name}` (named "
             "group), `$&` (the whole match), `$$` (a literal `$`)."),
        ),
        (
            ("Comme les autres regex, un scalaire est **converti en texte** (`42` devient "
             "`\"42\"`), là où `replace` rendrait `false`."),
            ("Like the other regex functions, a scalar is **converted to text** (`42` becomes "
             "`\"42\"`), where `replace` would return `false`."),
        ),
    ],
    "regexmatches": [
        (
            ("Dans une chaîne jslt, l'antislash se **double** : `\"\\\\d+\"`. Les groupes "
             "nommés s'écrivent `(?<nom>…)` ou `(?P<nom>…)`."),
            ("Inside a jslt string, backslashes are **doubled**: `\"\\\\d+\"`. Named groups are "
             "written `(?<name>…)` or `(?P<name>…)`."),
        ),
        (
            "`null`, un objet ou un tableau donnent `null` ; un motif invalide lève.",
            "`null`, an object or an array give `null`; an invalid pattern raises.",
        ),
    ],
    "convert": [
        (
            ("Types : `integer`, `decimal`, `string`, `boolean` — complets ; `uri`, `uuid`, "
             "`datetime`, `time` sont rendus **en texte** (le portage n'a pas ces types). La "
             "forme `$.x #integer` fait la même chose."),
            ("Types: `integer`, `decimal`, `string`, `boolean` — complete; `uri`, `uuid`, "
             "`datetime`, `time` are returned **as text** (the port has no such types). The "
             "`$.x #integer` form does the same."),
        ),
    ],
    "merge": [
        (
            ("Fusion **plate** par défaut : la droite remplace la clé entière. `deep` fusionne "
             "les sous-objets, `arrays` concatène les tableaux au lieu de les remplacer."),
            ("A **flat** merge by default: the right-hand side replaces the whole key. `deep` "
             "merges sub-objects, `arrays` concatenates arrays instead of replacing them."),
        ),
        (
            "Les sources ne sont **pas** modifiées : le résultat est un nouvel objet.",
            "The sources are **not** modified: the result is a new object.",
        ),
    ],
    "pick": [
        (
            ("Accepte une clé seule (`\"nom\"`) ou un tableau de clés. Une clé absente est "
             "ignorée, elle n'apparaît pas à `null` dans le résultat."),
            ("Accepts a single key (`\"name\"`) or an array of keys. A missing key is ignored: "
             "it does not appear as `null` in the result."),
        ),
    ],
    "omit": [
        (
            "Accepte une clé seule ou un tableau de clés ; retirer une clé absente ne lève pas.",
            "Accepts a single key or an array of keys; removing a missing key does not raise.",
        ),
    ],
    "has": [
        (
            ("`has` existe parce qu'`isnull` ne distingue pas une **clé absente** d'une clé "
             "présente **à `null`** : les deux donnent `true`, et ce n'est pas la même chose "
             "dans un flux."),
            ("`has` exists because `isnull` does not tell an **absent key** from a key present "
             "**with `null`**: both give `true`, and in a feed those are not the same thing."),
        ),
    ],
    "renamekeys": [
        (
            ("Une clé non mentionnée dans le mapping est **gardée telle quelle**. En cas de "
             "collision, le dernier écrit gagne : lever casserait une migration en cours."),
            ("A key not mentioned in the mapping is **kept as is**. On a collision the last "
             "write wins: raising would break a migration in progress."),
        ),
    ],
    "flattenobject": [
        (
            ("Les tableaux sont indexés par leur **position** (`l.0`, `l.1`) : c'est le pont "
             "vers un CSV, qui n'a pas de profondeur."),
            ("Arrays are indexed by **position** (`l.0`, `l.1`): this is the bridge to a CSV, "
             "which has no depth."),
        ),
    ],
    "unflatten": [
        (
            ("Les segments numériques ne redeviennent des **tableaux** que si `arrays` vaut "
             "`true` : une clé « 2026 » est un nom d'année dans la moitié des documents, et "
             "en faire un indice créerait un tableau de deux mille trous."),
            ("Numeric segments only become **arrays** when `arrays` is `true`: a key \"2026\" is "
             "a year's name in half of real documents, and turning it into an index would "
             "create an array with two thousand holes."),
        ),
        (
            "Un conflit de chemin (`a` valant 1 et `a.b` valant 2) **lève**.",
            "A path conflict (`a` being 1 and `a.b` being 2) **raises**.",
        ),
    ],
    "walk": [
        (
            ("Le parcours va des **feuilles vers la racine** : l'expression voit des enfants "
             "déjà transformés, donc une règle qui dépend d'eux fonctionne."),
            ("The walk goes from the **leaves to the root**: the expression sees already "
             "transformed children, so a rule that depends on them works."),
        ),
    ],
    "prune": [
        (
            ("Par défaut, seuls les `null` partent : `0`, `false` et `\"\"` sont des **valeurs**, "
             "et supprimer un « montant : 0 » perdrait une information."),
            ("By default only `null`s go: `0`, `false` and `\"\"` are **values**, and dropping an "
             "\"amount: 0\" would lose information."),
        ),
        (
            ("L'option `\"empty\"` retire en plus les chaînes, tableaux et objets vides — mais "
             "garde `0` et `false`."),
            ("The `\"empty\"` option also removes empty strings, arrays and objects — but keeps "
             "`0` and `false`."),
        ),
    ],
    "setpath": [
        (
            ("Rend une **copie** : la source n'est pas modifiée. Les niveaux manquants sont "
             "créés, et le séparateur est réglable (4e argument)."),
            ("Returns a **copy**: the source is not modified. Missing levels are created, and "
             "the separator is adjustable (4th argument)."),
        ),
    ],
    "unsetpath": [
        (
            "Rend une copie ; un chemin absent n'est **pas** une erreur.",
            "Returns a copy; a missing path is **not** an error.",
        ),
    ],
    "sort": [
        (
            ("L'ordre est **total** et ne lève jamais : `null` < booléens < nombres < chaînes "
             "< tableaux < objets. Les chaînes se comparent par **points de code** — pour un "
             "ordre humain, trier sur `foldtext($)`."),
            ("The order is **total** and never raises: `null` < booleans < numbers < strings < "
             "arrays < objects. Strings compare by **code point** — for a human order, sort on "
             "`foldtext($)`."),
        ),
        (
            ("Le tri est **stable** dans les deux sens : à clefs égales, l'ordre d'origine "
             "survit."),
            ("The sort is **stable** both ways: at equal keys, the original order survives."),
        ),
    ],
    "groupby": [
        (
            ("La clef est convertie en **texte**, puisqu'une clé d'objet JSON est une chaîne : "
             "une clef composite donne `[\"FR\",\"Lyon\"]` en JSON compact. `nested` évite d'avoir "
             "à la re-analyser."),
            ("The key is converted to **text**, since a JSON object key is a string: a "
             "composite key gives `[\"FR\",\"Lyon\"]` as compact JSON. `nested` saves you from "
             "parsing it back."),
        ),
    ],
    "sumby": [
        (
            ("Une valeur non numérique **lève**, comme pour `sum` : un total qui saute les "
             "intrus est plausible et faux."),
            ("A non-numeric value **raises**, as for `sum`: a total that skips the intruders is "
             "plausible and wrong."),
        ),
    ],
    "count": [
        (
            ("Compte les éléments d'un tableau, les **clés** d'un objet, les **caractères** "
             "d'un texte ; un scalaire vaut 1 (c'est une valeur) et `null` vaut 0 (c'est une "
             "absence)."),
            ("Counts the elements of an array, the **keys** of an object, the **characters** of "
             "a text; a scalar counts as 1 (it is a value) and `null` as 0 (it is an absence)."),
        ),
    ],
    "avg": [
        (
            ("Un tableau vide rend `null`, pas `0` : la moyenne de rien n'est pas zéro. Un "
             "élément non numérique lève."),
            ("An empty array gives `null`, not `0`: the mean of nothing is not zero. A "
             "non-numeric element raises."),
        ),
    ],
    "product": [
        (
            "Un tableau vide rend `1`, l'élément neutre — comme `sum([])` rend `0`.",
            "An empty array gives `1`, the neutral element — just as `sum([])` gives `0`.",
        ),
    ],
    "variance": [
        (
            ("De **population** par défaut : les données d'un template sont l'ensemble, pas un "
             "tirage. `sample` à `true` applique la correction de Bessel (n−1)."),
            ("Of the **population** by default: a template's data is the whole set, not a "
             "sample. `sample` set to `true` applies Bessel's correction (n−1)."),
        ),
    ],
    "percentile": [
        (
            ("Interpolation **linéaire** entre les deux rangs encadrants (méthode par défaut de "
             "NumPy) : `percentile(v, 50)` coïncide donc avec `median`."),
            ("**Linear** interpolation between the two surrounding ranks (NumPy's default "
             "method): so `percentile(v, 50)` coincides with `median`."),
        ),
    ],
    "mode": [
        (
            ("Accepte **toutes** les valeurs, pas seulement des nombres : la plus fréquente "
             "d'un libellé a un sens. À égalité, la **première apparue** gagne."),
            ("Accepts **any** values, not only numbers: the most frequent label is meaningful. "
             "On a tie, the **first seen** wins."),
        ),
    ],
    "min": [
        (
            ("Deux formes : deux nombres (résultat **décimal**) ou un tableau (le **type est "
             "conservé**). Un tableau *et* un second argument lève, plutôt que d'ignorer le "
             "second."),
            ("Two forms: two numbers (a **decimal** result) or an array (the **type is "
             "preserved**). An array *and* a second argument raises, rather than ignoring the "
             "second."),
        ),
    ],
    "max": [
        (
            ("Deux formes : deux nombres (résultat **décimal**) ou un tableau (le **type est "
             "conservé**). Un tableau *et* un second argument lève."),
            ("Two forms: two numbers (a **decimal** result) or an array (the **type is "
             "preserved**). An array *and* a second argument raises."),
        ),
    ],
    "round": [
        (
            ("Arrondi **bancaire** (au pair le plus proche) : `2.5` donne `2` et `3.5` donne "
             "`4`. Pour couper vers zéro, `truncate` ; vers le haut, `ceil`."),
            ("**Banker's** rounding (to the nearest even): `2.5` gives `2` and `3.5` gives `4`. "
             "To cut towards zero use `truncate`; upwards, `ceil`."),
        ),
    ],
    "tobase": [
        (
            ("Bases de 2 à 36 (chiffres puis lettres minuscules). `width` complète de zéros à "
             "gauche ; le signe est écrit **devant** les chiffres, un entier JSON n'ayant pas "
             "de largeur fixe."),
            ("Bases from 2 to 36 (digits then lower-case letters). `width` pads with leading "
             "zeros; the sign is written **in front of** the digits, a JSON integer having no "
             "fixed width."),
        ),
    ],
    "clamp": [
        (
            "Une valeur qui n'est pas un nombre rend `null` plutôt que d'être ramenée à une borne.",
            "A value that is not a number gives `null` rather than being brought back to a bound.",
        ),
    ],
    "urlencode": [
        (
            ("Le mode `\"path\"` **conserve les barres obliques** : c'est celui d'un chemin "
             "d'URL. Par défaut, elles sont encodées (`%2F`), ce qu'exige un paramètre."),
            ("The `\"path\"` mode **keeps the slashes**: that is the mode for a URL path. By "
             "default they are encoded (`%2F`), which is what a query parameter requires."),
        ),
    ],
    "sha256": [
        (
            ("Pour l'**identité** (comparer, indexer), jamais pour signer : concaténer un "
             "secret et un message avant un `sha256` expose à l'extension de longueur. Pour "
             "signer, `hmacsha256`."),
            ("For **identity** (comparing, indexing), never for signing: concatenating a secret "
             "and a message before a `sha256` exposes you to length extension. To sign, use "
             "`hmacsha256`."),
        ),
    ],
    "md5": [
        (
            "Pour l'**identité** seulement : MD5 est cassé pour toute usage de sécurité.",
            "For **identity** only: MD5 is broken for any security use.",
        ),
    ],
    "trydefault": [
        (
            ("Le repli n'est évalué **que** si la première expression lève : il peut donc être "
             "coûteux sans ralentir le cas nominal."),
            ("The fallback is evaluated **only** when the first expression raises: it can "
             "therefore be expensive without slowing the nominal case."),
        ),
        (
            ("Il n'attrape que les erreurs du moteur (`JsltError`), pas une valeur `null` : "
             "pour un repli sur l'absence, l'opérateur `??`."),
            ("It only catches engine errors (`JsltError`), not a `null` value: for a fallback "
             "on absence, use the `??` operator."),
        ),
    ],
    "parsejson": [
        (
            "Un texte illisible **lève** plutôt que de rendre `null` : la faute se voit là où elle est.",
            "Unreadable text **raises** rather than giving `null`: the fault shows where it is.",
        ),
    ],
    "require": [
        (
            ("Ne refuse que l'**absence** : `0`, `false` et `\"\"` sont des valeurs et passent. "
             "Pour une condition, `requirethat`."),
            ("Only refuses **absence**: `0`, `false` and `\"\"` are values and pass. For a "
             "condition, use `requirethat`."),
        ),
        (
            ("L'erreur est une `JsltError` porteuse du message : elle est donc rattrapable par "
             "`trydefault`."),
            ("The error is a `JsltError` carrying the message: it can therefore be caught by "
             "`trydefault`."),
        ),
    ],
    "requirethat": [
        (
            ("Exige `true` **strict** : une condition qui vaut `0` ou `\"\"` est refusée, parce "
             "que c'est presque toujours une expression qu'on croyait booléenne."),
            ("Requires a **strict** `true`: a condition worth `0` or `\"\"` is refused, because "
             "it is almost always an expression one believed to be boolean."),
        ),
    ],
    "trace": [
        (
            ("Le journal vit sur le **contexte d'exécution** : deux exécutions concurrentes ne "
             "se mélangent pas, et un intégrateur le lit après coup (`context.traces`) sans "
             "que le template ait à le recopier dans sa sortie."),
            ("The journal lives on the **execution context**: two concurrent runs never mix, "
             "and an integrator reads it afterwards (`context.traces`) without the template "
             "having to copy it into its output."),
        ),
    ],
    "isiban": [
        (
            ("Vérifie la structure et la **clé modulo 97**, mais pas la longueur par pays : ce "
             "serait une table de soixante entrées dont la péremption ferait refuser un IBAN "
             "valide."),
            ("Checks the structure and the **modulo-97 check digits**, but not the per-country "
             "length: that would be a sixty-entry table whose staleness would reject a valid "
             "IBAN."),
        ),
    ],
    "isemail": [
        (
            ("Volontairement **pragmatique** : la RFC 5322 complète accepte des formes que "
             "personne n'utilise, et les accepter laisserait passer ce qu'un système en aval "
             "refusera."),
            ("Deliberately **pragmatic**: the full RFC 5322 accepts forms nobody uses, and "
             "accepting them would let through what a downstream system will reject."),
        ),
    ],
    "to_csv": [
        (
            ("Les colonnes sont l'**union des clés** rencontrées, dans l'ordre d'apparition : "
             "s'arrêter au premier objet perdrait des données sur un flux hétérogène."),
            ("The columns are the **union of the keys** encountered, in order of appearance: "
             "stopping at the first object would lose data on a heterogeneous feed."),
        ),
        (
            ("Les valeurs imbriquées sont aplaties en clés pointées (`flattenobject`), les "
             "guillemets doublés et les lignes finies en CRLF, comme l'exige la RFC 4180."),
            ("Nested values are flattened into dotted keys (`flattenobject`), quotes are "
             "doubled and lines end with CRLF, as RFC 4180 requires."),
        ),
    ],
    "to_xml": [
        (
            ("Conventions de `parsexml` : une clé préfixée `@` devient un **attribut**, `#text` "
             "le contenu textuel, et une clé dont la valeur est un tableau **répète** "
             "l'élément. Un nom d'élément invalide lève."),
            ("`parsexml` conventions: a key prefixed with `@` becomes an **attribute**, `#text` "
             "the textual content, and a key whose value is an array **repeats** the element. "
             "An invalid element name raises."),
        ),
    ],
    "to_yaml": [
        (
            ("Sous-ensemble assumé : ni ancres, ni tags, ni littéral multi-ligne. Tout scalaire "
             "relisible comme un autre type est **cité** — un texte `\"true\"` ou `\"12\"` reste un "
             "texte."),
            ("An acknowledged subset: no anchors, no tags, no multi-line literal. Any scalar "
             "that would read back as another type is **quoted** — a `\"true\"` or `\"12\"` text "
             "stays text."),
        ),
    ],
    "to_json": [
        (
            ("`ignore_null_and_empty_value` transforme les chaînes vides en `null` **puis** "
             "retire les propriétés nulles des objets ; les tableaux gardent leurs éléments."),
            ("`ignore_null_and_empty_value` turns empty strings into `null` **then** removes "
             "null properties from objects; arrays keep their elements."),
        ),
    ],
    "zip": [
        (
            ("S'arrête au plus court plutôt que de compléter par `null` : un appariement "
             "inventé serait indiscernable d'une vraie valeur nulle."),
            ("Stops at the shorter one rather than padding with `null`: an invented pair would "
             "be indistinguishable from a genuine null value."),
        ),
    ],
    "chunk": [
        (
            "Une taille nulle ou négative **lève** : c'est une faute d'écriture, pas une donnée surprenante.",
            "A zero or negative size **raises**: that is an authoring mistake, not surprising data.",
        ),
    ],
    "intersect": [
        (
            ("Égalité **structurelle** (et non `==`, où `\"2\" == 2`), ordre de gauche conservé, "
             "doublons retirés."),
            ("**Structural** equality (not `==`, where `\"2\" == 2`), left order preserved, "
             "duplicates removed."),
        ),
    ],
    "contains": [
        (
            ("Garde l'égalité `==` du langage, où `\"2\" == 2` est **vrai**. Pour une égalité "
             "structurelle, `indexof(l, v) != -1`."),
            ("Keeps the language's `==` equality, where `\"2\" == 2` is **true**. For structural "
             "equality, use `indexof(l, v) != -1`."),
        ),
    ],
    "group": [
        (
            ("Rend des groupes `{Label, Items}`, imbriqués quand plusieurs chemins sont donnés. "
             "`groupby` rend un **objet**, réductible par `entries`."),
            ("Returns `{Label, Items}` groups, nested when several paths are given. `groupby` "
             "returns an **object**, reducible with `entries`."),
        ),
    ],
    "join": [
        (
            ("Jointure **gauche** : chaque objet de gauche reçoit, sous `Name`, les éléments de "
             "`Source` dont `Key` est égale (comparée en texte). La source n'est pas modifiée."),
            ("A **left** join: each left object receives, under `Name`, the elements of `Source` "
             "whose `Key` is equal (compared as text). The source is not modified."),
        ),
    ],
    "createindex": [
        (
            ("Se range dans une variable (`\"i:\": createindex(…)`) que `index(i:, clé)` "
             "interroge ensuite. Le 2e argument est le chemin de **découpe** (vide = la source "
             "entière)."),
            ("Goes into a variable (`\"i:\": createindex(…)`) that `index(i:, key)` then queries. "
             "The 2nd argument is the **splitting** path (empty = the whole source)."),
        ),
    ],
    "parsedate": [
        (
            ("**Sans masque, seules les formes numériques et l'ISO 8601 sont reconnues.** "
            "`parsedate($.t, \"en-US\")` sur « November 11, 2026 » lève `date illisible` : "
            "un mois ou un jour **en lettres** demande un masque (`MMMM`, `MMM`, `dddd`, "
            "`ddd`)."),
            ("**With no mask, only numeric forms and ISO 8601 are recognised.** "
            "`parsedate($.t, \"en-US\")` on \"November 11, 2026\" raises `date illisible`: "
            "a month or a day **spelled out** requires a mask (`MMMM`, `MMM`, `dddd`, "
            "`ddd`)."),
        ),
        (
            ("Le vocabulaire complet des jetons — et ce que chacun lit — est dans "
            "[Masques de date](../dates.md#masques-de-date). Il est **commun** avec "
            "`format` : ce qui s'écrit se relit."),
            ("The full token vocabulary — and what each one reads — is in "
            "[Date masks](../dates.en.md#date-masks). It is **shared** with `format`: what "
            "is written can be read back."),
        ),
        (
            ("Les largeurs sont **strictes** : `dd` exige deux chiffres, `d` en accepte un "
            "ou deux. `1/2/26` n'est donc pas conforme à `dd/MM/yyyy`, et lève."),
            ("Widths are **strict**: `dd` requires two digits, `d` accepts one or two. So "
            "`1/2/26` does not match `dd/MM/yyyy`, and raises."),
        ),
        (
            ("`ddd` / `dddd` (le nom du jour) sont **lus puis ignorés** : ils servent à ce "
            "que le masque colle au texte, pas à décider la date."),
            ("`ddd` / `dddd` (the day name) are **read then ignored**: they are there so the "
            "mask matches the text, not to decide the date."),
        ),
        (
            ("Les noms de mois et de jours, le séparateur de date et le désignateur AM/PM "
            "viennent de la **culture** (2e argument) : c'est elle qui dit si `MMMM` lit "
            "« November » ou « novembre ». Cultures : vide (invariante, anglais), `en-US`, "
            "`en-GB`, `fr-FR`, `de-DE`, `es-ES`, `it-IT`."),
            ("The month and day names, the date separator and the AM/PM designator come from "
            "the **culture** (2nd argument): it decides whether `MMMM` reads \"November\" or "
            "\"novembre\". Cultures: empty (invariant, English), `en-US`, `en-GB`, `fr-FR`, "
            "`de-DE`, `es-ES`, `it-IT`."),
        ),
        (
            ("`null` donne `null`. Un texte qui n'est pas une date **lève** plutôt que de "
            "rendre une date fausse ou « aujourd'hui » : la faute se voit là où elle est."),
            ("`null` gives `null`. Text that is not a date **raises** rather than returning a "
            "wrong date or \"today\": the fault shows where it is."),
        ),
    ],
    "format": [
        (
            ("Le tableau complet des masques — nombres, dates, cultures — est dans "
            "[Formatage](../texte.md#formatage--format)."),
            ("The full mask table — numbers, dates, cultures — is in "
            "[Formatting](../texte.en.md#formatting-format)."),
        ),
        (
            ("Une chaîne **ISO 8601 est une date** : `format($.d, \"dd/MM/yyyy\")` la formate "
            "comme telle, sans conversion préalable."),
            ("An **ISO 8601 string is a date**: `format($.d, \"dd/MM/yyyy\")` formats it as "
            "such, with no prior conversion."),
        ),
        (
            ("La culture décide des séparateurs : `#,##0.00` rend `1 234,50` en `fr-FR` et "
            "`1,234.50` en `en-US`. Le masque, lui, ne change pas."),
            ("The culture decides the separators: `#,##0.00` returns `1 234,50` in `fr-FR` "
            "and `1,234.50` in `en-US`. The mask itself does not change."),
        ),
        (
            ("Un masque hors du sous-ensemble géré **lève**, plutôt que de rendre un texte "
            "approximatif qu'on ne verrait qu'en production."),
            ("A mask outside the supported subset **raises**, rather than returning an "
            "approximate text that would only be noticed in production."),
        ),
    ],
    "dateadd": [
        (
            ("`month` et `year` sont **calendaires** : le jour est **borné** sur les mois "
            "courts, donc le 31 janvier + 1 mois donne le 28 février, et non le 3 mars."),
            ("`month` and `year` are **calendar** units: the day is **clamped** on short "
            "months, so 31 January + 1 month gives 28 February, not 3 March."),
        ),
        (
            ("Conséquence : `dateadd` et `datediff` ne sont **pas** exactement inverses l'un "
            "de l'autre sur ces deux unités."),
            ("Consequence: `dateadd` and `datediff` are **not** exact inverses of each other "
            "on those two units."),
        ),
    ],
    "datediff": [
        (
            ("Le compte est en unités **entières écoulées**, tronquées **vers zéro** : du 15 "
            "janvier au 14 février il y a `0` mois, et au 15 février `1`."),
            ("The count is in **whole elapsed** units, truncated **towards zero**: from 15 "
            "January to 14 February there are `0` months, and to 15 February `1`."),
        ),
        (
            ("Comparer une date **avec** fuseau à une date **sans** fuseau lève : l'écart "
            "n'aurait pas de sens, et le supposer donnerait un résultat faux de quelques "
            "heures."),
            ("Comparing a date **with** a timezone to one **without** raises: the difference "
            "would be meaningless, and assuming one would be wrong by a few hours."),
        ),
    ],
    "datepart": [
        (
            ("`dayofweek` numérote à partir de **dimanche = 0** (samedi = 6), alors que "
            "`datestartof(…, \"week\")` commence **lundi** (ISO). Les deux conventions "
            "coexistent : la première nomme un jour, la seconde borne une semaine."),
            ("`dayofweek` numbers from **Sunday = 0** (Saturday = 6), whereas "
            "`datestartof(…, \"week\")` starts on **Monday** (ISO). Both conventions coexist: "
            "the first names a day, the second bounds a week."),
        ),
        (
            ("Parties disponibles : `year`, `quarter`, `month`, `day`, `dayofweek`, "
            "`dayofyear`, `week`, `hour`, `minute`, `second`."),
            ("Available parts: `year`, `quarter`, `month`, `day`, `dayofweek`, `dayofyear`, "
            "`week`, `hour`, `minute`, `second`."),
        ),
    ],
    "datestartof": [
        (
            ("La semaine commence **lundi** (ISO). Périodes : `year`, `quarter`, `month`, "
            "`week`, `day`, `hour`, `minute`."),
            ("The week starts on **Monday** (ISO). Periods: `year`, `quarter`, `month`, "
            "`week`, `day`, `hour`, `minute`."),
        ),
    ],
    "dateendof": [
        (
            ("La borne est **inclusive**, à la microseconde près : la fin d'un jour est "
            "`23:59:59.999999`, et non le début du lendemain. Un filtre `<=` attrape donc "
            "toute la journée."),
            ("The bound is **inclusive**, to the microsecond: the end of a day is "
            "`23:59:59.999999`, not the start of the next one. So a `<=` filter catches the "
            "whole day."),
        ),
    ],
    "datezone": [
        (
            ("Sur une date **sans** décalage, le fuseau est **attribué** (la date ne bouge "
            "pas) ; sur une date qui en porte un, elle est **convertie** (l'instant ne bouge "
            "pas). Noms IANA (`Europe/Paris`), `UTC`, ou décalage fixe (`+02:00`)."),
            ("On a date **without** an offset, the timezone is **attached** (the date does not "
            "move); on one that carries an offset, the date is **converted** (the instant "
            "does not move). IANA names (`Europe/Paris`), `UTC`, or a fixed offset "
            "(`+02:00`)."),
        ),
    ],
    "dateduration": [
        (
            ("Le résultat porte `negative` : l'intervalle est décomposé en valeurs positives, "
            "et c'est ce drapeau qui dit dans quel sens il va."),
            ("The result carries `negative`: the interval is broken down into positive values, "
            "and that flag says which way it goes."),
        ),
    ],
    "now": [
        (
            ("Non déterministe : deux appels dans le même template peuvent différer. Pour un "
            "template **testable**, passer l'instant en paramètre externe "
            "(`param(\"date_reference\")`) plutôt que d'appeler `now()`."),
            ("Non-deterministic: two calls in the same template may differ. For a **testable** "
            "template, pass the instant as an external parameter "
            "(`param(\"reference_date\")`) rather than calling `now()`."),
        ),
    ],
    "today": [
        (
            ("Minuit **local**, ou UTC si `utc` vaut `true`. Comme `now`, elle rend un "
            "template non déterministe : préférer un paramètre externe quand le résultat doit "
            "être reproductible."),
            ("**Local** midnight, or UTC when `utc` is `true`. Like `now`, it makes a template "
            "non-deterministic: prefer an external parameter when the result must be "
            "reproducible."),
        ),
    ],
    "ifelse": [
        (
            ("Seule la branche **retenue** est évaluée : `ifelse($.d == 0, 0, 100 / $.d)` ne "
             "divise pas par zéro. C'est tout l'intérêt de la fonction, et ce qu'un opérateur "
             "à arguments évalués ne pourrait pas offrir."),
            ("Only the **chosen** branch is evaluated: `ifelse($.d == 0, 0, 100 / $.d)` does "
             "not divide by zero. That is the whole point of the function, and what an "
             "operator with evaluated arguments could not offer."),
        ),
        (
            ("`when` aiguille sur une **valeur** (`==` contre chaque nom de cas) ; `ifelse` "
             "teste une **condition**, donc une expression composée. Pour plus de deux cas, "
             "`ifelse` s'imbrique."),
            ("`when` switches on a **value** (`==` against each case name); `ifelse` tests a "
             "**condition**, hence a composed expression. For more than two cases, `ifelse` "
             "nests."),
        ),
    ],
    "get": [
        (
            ("Clef absente, indice hors bornes, source qui n'est ni objet ni tableau : `null`. "
             "Il n'y a donc pas d'argument de repli — `get($.o, $.k) ?? 0` le dit, et un repli "
             "en argument serait évalué même quand la clef existe."),
            ("Missing key, out-of-bounds index, source that is neither object nor array: "
             "`null`. There is therefore no fallback argument — `get($.o, $.k) ?? 0` says it, "
             "and a fallback as an argument would be evaluated even when the key exists."),
        ),
        (
            ("Pour **exiger** la valeur : `require(get($.o, $.k), \"tarif inconnu\")`. Pour "
             "distinguer une clef absente d'une clef présente valant `null` : `has`."),
            ("To **require** the value: `require(get($.o, $.k), \"unknown price\")`. To tell a "
             "missing key from a key present but null: `has`."),
        ),
    ],
    "getpath": [
        (
            ("Réciproque de `setpath`, qui n'en avait pas : les étapes se lisent de la même "
             "façon, indices de tableau compris (`\"lignes.0.ref\"`)."),
            ("The reciprocal of `setpath`, which had none: the steps read the same way, array "
             "indices included (`\"lignes.0.ref\"`)."),
        ),
        (
            ("Une étape manquante — ou un scalaire rencontré en cours de route — rend `null` "
             "sans lever : c'est la sémantique d'un chemin, et `??` fournit le repli."),
            ("A missing step — or a scalar met along the way — gives `null` without raising: "
             "that is a path's semantics, and `??` provides the fallback."),
        ),
    ],
    "roundhalfup": [
        (
            ("L'arrondi **commercial**, là où `round` est bancaire : `round(0.125, 2)` rend "
             "`0.12`. Les demis **s'éloignent de zéro**, donc `-0.5` rend `-1` — un avoir "
             "s'arrondit comme la facture qu'il annule."),
            ("**Commercial** rounding, where `round` is banker's: `round(0.125, 2)` gives "
             "`0.12`. Halves go **away from zero**, so `-0.5` gives `-1` — a credit note "
             "rounds like the invoice it cancels."),
        ),
        (
            ("Le nombre est lu tel qu'il est **écrit** : `2.675` se stocke en `2.67499999…`, "
             "et un arrondi conduit sur cette valeur rendrait `2.67`."),
            ("The number is read as it is **written**: `2.675` is stored as `2.67499999…`, and "
             "a rounding run on that value would give `2.67`."),
        ),
    ],
    "roundto": [
        (
            ("Un pas nul ou négatif **lève**, plutôt que de rendre une valeur qui n'a été "
             "arrondie à rien — ce qu'un `roundto($.n, $.pas)` au pas absent produirait."),
            ("A zero or negative step **raises**, rather than returning a value that was "
             "rounded to nothing — which a `roundto($.n, $.step)` with a missing step would "
             "produce."),
        ),
        (
            ("Les demis s'éloignent de zéro, comme `roundhalfup`, et le calcul ne passe pas "
             "par un flottant intermédiaire : le contournement `round($.n * 20) / 20` le "
             "faisait, avec l'erreur de représentation qui va avec."),
            ("Halves go away from zero, like `roundhalfup`, and the computation goes through "
             "no intermediate float: the workaround `round($.n * 20) / 20` did, with the "
             "representation error that comes with it."),
        ),
    ],
    "toprecision": [
        (
            ("Chiffres **significatifs**, pas décimales : `round($.n, 2)` fixe le rang de la "
             "virgule, ce qui n'a pas de sens sur une colonne où voisinent `0.00241` et "
             "`24100`."),
            ("**Significant** digits, not decimals: `round($.n, 2)` fixes where the decimal "
             "point falls, which makes no sense in a column where `0.00241` sits next to "
             "`24100`."),
        ),
        (
            ("Moins d'un chiffre **lève** ; `0` est rendu tel quel, un zéro ayant autant de "
             "chiffres significatifs qu'on veut."),
            ("Fewer than one digit **raises**; `0` is returned as is, since zero has as many "
             "significant digits as one likes."),
        ),
    ],
    "stringlength": [
        (
            ("Même fonction que `stringlenght`, dont l'orthographe d'origine est fautive : "
             "les deux noms enregistrent la **même** implémentation, donc ils ne peuvent pas "
             "diverger. Retirer l'ancien casserait les templates écrits avec."),
            ("The same function as `stringlenght`, whose original spelling is a typo: both "
             "names register the **same** implementation, so they cannot diverge. Removing "
             "the old one would break the templates written with it."),
        ),
    ],
}

#: name -> liste d'exemples (un seul, sauf quand deux usages se répondent).
#: Un exemple peut porter un commentaire (`note` + `note_en`, les deux ou
#: aucun) : il se lit AVANT le template, pour savoir ce qu'on regarde.
EXAMPLES: dict[str, list[dict[str, str]]] = {
    # --- maths ----------------------------------------------------------------
    "abs": [{"template": '{ "r": abs($.n) }', "source": '{ "n": -3.5 }', "output": '{ "r": 3.5 }'}],
    "acos": [{"template": '{ "r": acos($.n) }', "source": '{ "n": 1 }', "output": '{ "r": 0.0 }'}],
    "acosh": [{"template": '{ "r": acosh($.n) }', "source": '{ "n": 1 }', "output": '{ "r": 0.0 }'}],
    "asin": [{"template": '{ "r": asin($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 0.0 }'}],
    "asinh": [{"template": '{ "r": asinh($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 0.0 }'}],
    "atan": [{"template": '{ "r": atan($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 0.0 }'}],
    "atan2": [{"template": '{ "r": atan2($.y, $.x) }', "source": '{ "y": 0, "x": 1 }', "output": '{ "r": 0.0 }'}],
    "atanh": [{"template": '{ "r": atanh($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 0.0 }'}],
    "ceil": [
        {
            "template": '{ "entier": ceil($.n), "deux_decimales": ceil($.n, 2) }',
            "source": '{ "n": 2.341 }',
            "output": '{ "entier": 3.0, "deux_decimales": 2.35 }',
        }
    ],
    "cos": [{"template": '{ "r": cos($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 1.0 }'}],
    "cosh": [{"template": '{ "r": cosh($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 1.0 }'}],
    "e": [{"template": '{ "r": round(e(), 3) }', "source": "{}", "output": '{ "r": 2.718 }'}],
    "exp": [{"template": '{ "r": round(exp($.n), 3) }', "source": '{ "n": 1 }', "output": '{ "r": 2.718 }'}],
    "floor": [
        {
            "template": '{ "entier": floor($.n), "deux_decimales": floor($.n, 2) }',
            "source": '{ "n": 2.349 }',
            "output": '{ "entier": 2.0, "deux_decimales": 2.34 }',
        }
    ],
    "logarithm": [{"template": '{ "r": logarithm($.n) }', "source": '{ "n": 1 }', "output": '{ "r": 0.0 }'}],
    "logarithm10": [{"template": '{ "r": logarithm10($.n) }', "source": '{ "n": 1000 }', "output": '{ "r": 3.0 }'}],
    "logarithm2": [{"template": '{ "r": logarithm2($.n) }', "source": '{ "n": 8 }', "output": '{ "r": 3.0 }'}],
    "max": [
        {
            "template": '{ "deux": max($.a, $.b), "du_tableau": max($.l) }',
            "source": '{ "a": 2, "b": 9, "l": [3, 11, 7] }',
            "output": '{ "deux": 9.0, "du_tableau": 11 }',
        }
    ],
    "min": [
        {
            "template": '{ "deux": min($.a, $.b), "du_tableau": min($.l) }',
            "source": '{ "a": 2, "b": 9, "l": [3, 11, 7] }',
            "output": '{ "deux": 2.0, "du_tableau": 3 }',
        }
    ],
    "pi": [{"template": '{ "r": round(pi(), 4) }', "source": "{}", "output": '{ "r": 3.1416 }'}],
    "pow": [{"template": '{ "r": pow($.b, $.e) }', "source": '{ "b": 2, "e": 10 }', "output": '{ "r": 1024.0 }'}],
    "round": [
        {
            "template": '{ "pair": round($.a), "deux_decimales": round($.b, 2) }',
            "source": '{ "a": 2.5, "b": 1.2345 }',
            "output": '{ "pair": 2.0, "deux_decimales": 1.23 }',
        }
    ],
    "sin": [{"template": '{ "r": sin($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 0.0 }'}],
    "sinh": [{"template": '{ "r": sinh($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 0.0 }'}],
    "sqrt": [{"template": '{ "r": sqrt($.n) }', "source": '{ "n": 9 }', "output": '{ "r": 3.0 }'}],
    "tan": [{"template": '{ "r": tan($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 0.0 }'}],
    "tanh": [{"template": '{ "r": tanh($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 0.0 }'}],
    "truncate": [
        {
            "template": '{ "vers_zero": truncate($.n), "deux_decimales": truncate($.n, 2) }',
            "source": '{ "n": -2.789 }',
            "output": '{ "vers_zero": -2.0, "deux_decimales": -2.78 }',
        }
    ],
    # --- nombres ---------------------------------------------------------------
    "clamp": [
        {
            "template": '{ "r": clamp($.n, 0, 100) }',
            "source": '{ "n": 142 }',
            "output": '{ "r": 100 }',
        }
    ],
    "frombase": [{"template": '{ "r": frombase($.t, 2) }', "source": '{ "t": "1011" }', "output": '{ "r": 11 }'}],
    "fromhex": [{"template": '{ "r": fromhex($.t) }', "source": '{ "t": "0xff" }', "output": '{ "r": 255 }'}],
    "gcd": [{"template": '{ "r": gcd($.a, $.b) }', "source": '{ "a": 84, "b": 36 }', "output": '{ "r": 12 }'}],
    "isfinite": [
        {
            "template": '{ "nombre": isfinite($.n), "texte": isfinite($.t) }',
            "source": '{ "n": 3, "t": "3" }',
            "output": '{ "nombre": true, "texte": false }',
        }
    ],
    "isnan": [
        {
            "template": '{ "r": isnan($.n) }',
            "source": '{ "n": 3 }',
            "output": '{ "r": false }',
        }
    ],
    "log": [{"template": '{ "r": log($.n, 10) }', "source": '{ "n": 1000 }', "output": '{ "r": 3.0 }'}],
    "parsenumber": [
        {
            "template": '{ "r": parsenumber($.t, "fr-FR") }',
            "source": '{ "t": "1 234,56" }',
            "output": '{ "r": 1234.56 }',
        }
    ],
    "shiftleft": [{"template": '{ "r": shiftleft($.n, 3) }', "source": '{ "n": 1 }', "output": '{ "r": 8 }'}],
    "shiftright": [{"template": '{ "r": shiftright($.n, 3) }', "source": '{ "n": 64 }', "output": '{ "r": 8 }'}],
    "sign": [
        {
            "template": '{ "negatif": sign($.a), "zero": sign($.b), "positif": sign($.c) }',
            "source": '{ "a": -4, "b": 0, "c": 7 }',
            "output": '{ "negatif": -1, "zero": 0, "positif": 1 }',
        }
    ],
    "tobase": [
        {
            "template": '{ "binaire": tobase($.n, 2), "sur_huit": tobase($.n, 2, 8) }',
            "source": '{ "n": 11 }',
            "output": '{ "binaire": "1011", "sur_huit": "00001011" }',
        }
    ],
    "tohex": [
        {
            "template": '{ "r": tohex($.n), "sur_quatre": tohex($.n, 4) }',
            "source": '{ "n": 255 }',
            "output": '{ "r": "ff", "sur_quatre": "00ff" }',
        }
    ],
    # --- parcours par expression -------------------------------------------------------
    "map": [
        {
            "note": "Ce que la boucle fait déjà — mais utilisable **en argument**.",
            "note_en": "What the loop already does — but usable **as an argument**.",
            "template": '{ "noms": map($.l, $.n), "total": sum(map($.l, $.age)) }',
            "source": '{ "l": [{ "n": "Ana", "age": 30 }, { "n": "Bo", "age": 25 }] }',
            "output": '{ "noms": ["Ana", "Bo"], "total": 55 }',
        }
    ],
    "filter": [
        {
            "note": "L'expression est quelconque : un filtre JSONPath ne sait pas appeler une fonction.",
            "note_en": "The expression is arbitrary: a JSONPath filter cannot call a function.",
            "template": '{ "r": filter($.l, stringcontains($.n, "a")) }',
            "source": '{ "l": [{ "n": "Ana" }, { "n": "Bo" }] }',
            "output": '{ "r": [{ "n": "Ana" }] }',
        }
    ],
    "find": [
        {
            "template": '{ "trouve": find($.l, $ > 2), "aucun": find($.l, $ > 9) }',
            "source": '{ "l": [1, 2, 3, 4] }',
            "output": '{ "trouve": 3, "aucun": null }',
        }
    ],
    "findindex": [
        {
            "template": '{ "position": findindex($.l, $ > 2), "aucune": findindex($.l, $ > 9) }',
            "source": '{ "l": [1, 2, 3, 4] }',
            "output": '{ "position": 2, "aucune": -1 }',
        }
    ],
    "every": [
        {
            "note": "Vrai sur un tableau **vide** : il n'y a aucun contre-exemple.",
            "note_en": "True on an **empty** array: there is no counter-example.",
            "template": '{ "tous": every($.l, $ > 0), "vide": every($.v, $ > 0) }',
            "source": '{ "l": [1, 2], "v": [] }',
            "output": '{ "tous": true, "vide": true }',
        }
    ],
    "some": [
        {
            "note": "`any` dit « tableau non vide » ; `some` teste un prédicat.",
            "note_en": "`any` says \"non-empty array\"; `some` tests a predicate.",
            "template": '{ "some": some($.l, $ > 3), "any": any($.l) }',
            "source": '{ "l": [1, 2] }',
            "output": '{ "some": false, "any": true }',
        }
    ],
    "reduce": [
        {
            "note": "L'expression voit `{acc, value, index}` et rend le nouvel accumulateur.",
            "note_en": "The expression sees `{acc, value, index}` and returns the new accumulator.",
            "template": '{ "somme": reduce($.l, $.acc + $.value, 0), "colle": reduce($.t, $.acc + $.value, "") }',
            "source": '{ "l": [1, 2, 3, 4], "t": ["a", "b", "c"] }',
            "output": '{ "somme": 10, "colle": "abc" }',
        },
        {
            "note": "Sans valeur initiale, le repli part du **premier élément**.",
            "note_en": "With no initial value, the fold starts from the **first element**.",
            "template": '{ "r": reduce($.l, max($.acc, $.value)) }',
            "source": '{ "l": [3, 9, 2] }',
            "output": '{ "r": 9.0 }',
        },
    ],
    "minby": [
        {
            "note": "Rend l'**élément**, là où `min` rend la valeur extrême sans dire qui la porte.",
            "note_en": "Returns the **element**, where `min` returns the extreme value without saying who carries it.",
            "template": '{ "r": map([minby($.l, $.prix)], $.ref) }',
            "source": '{ "l": [{ "ref": "A", "prix": 30 }, { "ref": "B", "prix": 10 }] }',
            "output": '{ "r": ["B"] }',
        }
    ],
    "maxby": [
        {
            "template": '{ "r": map([maxby($.l, $.prix)], $.ref) }',
            "source": '{ "l": [{ "ref": "A", "prix": 30 }, { "ref": "B", "prix": 10 }] }',
            "output": '{ "r": ["A"] }',
        }
    ],
    "cumsum": [
        {
            "template": '{ "r": cumsum($.l) }',
            "source": '{ "l": [1, 2, 3, 4] }',
            "output": '{ "r": [1, 3, 6, 10] }',
        }
    ],
    # --- construire et retoucher un tableau ---------------------------------------------
    "range": [
        {
            "note": "La **fin est exclue**, et un seul argument compte depuis zéro.",
            "note_en": "The **end is excluded**, and a single argument counts from zero.",
            "template": '{ "depuis_zero": range(5), "bornes": range(2, 5), "pas": range(0, 10, 3), "descendant": range(3, 0, -1) }',
            "source": "{}",
            "output": '{ "depuis_zero": [0, 1, 2, 3, 4], "bornes": [2, 3, 4], "pas": [0, 3, 6, 9], "descendant": [3, 2, 1] }',
        },
        {
            "note": "Seule fonction qui **crée** une série : tout le reste transforme ce qui entre.",
            "note_en": "The only function that **creates** a series: everything else transforms what comes in.",
            "template": '{ "carres": map(range(1, 5), $ * $) }',
            "source": "{}",
            "output": '{ "carres": [1, 4, 9, 16] }',
        },
    ],
    "slice": [
        {
            "note": "Fin exclue, indices négatifs depuis la fin, bornes trop larges tolérées.",
            "note_en": "End excluded, negative indices from the end, over-wide bounds tolerated.",
            "template": '{ "milieu": slice($.l, 1, 3), "fin": slice($.l, -2), "trop_loin": slice($.l, 9) }',
            "source": '{ "l": [1, 2, 3, 4, 5] }',
            "output": '{ "milieu": [2, 3], "fin": [4, 5], "trop_loin": [] }',
        }
    ],
    "append": [
        {
            "note": "Ajoute **une** valeur ; un tableau ajouté devient un élément imbriqué.",
            "note_en": "Adds **one** value; an array added becomes a nested element.",
            "template": '{ "valeur": append($.l, 3), "tableau": append($.l, [3, 4]), "source": $.l }',
            "source": '{ "l": [1, 2] }',
            "output": '{ "valeur": [1, 2, 3], "tableau": [1, 2, [3, 4]], "source": [1, 2] }',
        }
    ],
    "insert": [
        {
            "template": '{ "debut": insert($.l, 0, 9), "avant_dernier": insert($.l, -1, 9) }',
            "source": '{ "l": [1, 2] }',
            "output": '{ "debut": [9, 1, 2], "avant_dernier": [1, 9, 2] }',
        }
    ],
    "removeat": [
        {
            "note": "Un indice hors bornes rend la copie **inchangée**, il ne lève pas.",
            "note_en": "An out-of-range index returns the copy **unchanged**, it does not raise.",
            "template": '{ "sans_le_second": removeat($.l, 1), "dernier": removeat($.l, -1), "hors_bornes": removeat($.l, 9) }',
            "source": '{ "l": [1, 2, 3] }',
            "output": '{ "sans_le_second": [1, 3], "dernier": [1, 2], "hors_bornes": [1, 2, 3] }',
        }
    ],
    # --- découper un texte ---------------------------------------------------------------
    "chars": [
        {
            "note": "Par **graphème** : un « e » suivi d'un accent combinant reste un caractère.",
            "note_en": "By **grapheme**: an \"e\" followed by a combining accent stays one character.",
            "template": '{ "r": chars($.t) }',
            "source": '{ "t": "été" }',
            "output": '{ "r": ["é", "t", "é"] }',
        }
    ],
    "lines": [
        {
            "note": "Les trois fins de ligne, et les lignes **vides** sont gardées.",
            "note_en": "All three line endings, and **empty** lines are kept.",
            "template": '{ "r": lines($.t) }',
            "source": '{ "t": "a\\nb\\n\\nc" }',
            "output": '{ "r": ["a", "b", "", "c"] }',
        }
    ],
    "words": [
        {
            "template": '{ "r": words($.t) }',
            "source": '{ "t": "  le   petit chat " }',
            "output": '{ "r": ["le", "petit", "chat"] }',
        }
    ],
    "removeprefix": [
        {
            "note": (
                "Un **affixe entier**, là où `trimstart` retire un jeu de caractères : sur "
                "« bacab », `trimstart($.t, \"ab\")` rend « cab » alors que le préfixe n'y est pas."
            ),
            "note_en": (
                "A **whole affix**, where `trimstart` removes a set of characters: on "
                "\"bacab\", `trimstart($.t, \"ab\")` returns \"cab\" although the prefix is not there."
            ),
            "template": '{ "present": removeprefix($.t, "ba"), "absent": removeprefix($.t, "ab"), "jeu": trimstart($.t, "ab") }',
            "source": '{ "t": "bacab" }',
            "output": '{ "present": "cab", "absent": "bacab", "jeu": "cab" }',
        }
    ],
    "removesuffix": [
        {
            "template": '{ "present": removesuffix($.t, ".json"), "absent": removesuffix($.t, ".xml") }',
            "source": '{ "t": "contrat.json" }',
            "output": '{ "present": "contrat", "absent": "contrat.json" }',
        }
    ],
    "capitalize": [
        {
            "note": "La première lettre **seulement** ; `titlecase` met toutes les initiales.",
            "note_en": "The first letter **only**; `titlecase` upper-cases every initial.",
            "template": '{ "cap": capitalize($.t), "titre": titlecase($.t) }',
            "source": '{ "t": "bonjour le MONDE" }',
            "output": '{ "cap": "Bonjour le MONDE", "titre": "Bonjour Le MONDE" }',
        }
    ],
    # --- texte -----------------------------------------------------------------
    "endswith": [
        {
            "template": '{ "r": endswith($.t, ".json") }',
            "source": '{ "t": "contrat.json" }',
            "output": '{ "r": true }',
        }
    ],
    "indexof": [
        {
            "template": '{ "texte": indexof($.t, "o"), "tableau": indexof($.l, "b") }',
            "source": '{ "t": "bonjour", "l": ["a", "b", "c"] }',
            "output": '{ "texte": 1, "tableau": 1 }',
        }
    ],
    "lastindexof": [
        {
            "template": '{ "r": lastindexof($.t, "o") }',
            "source": '{ "t": "bonjour" }',
            "output": '{ "r": 4 }',
        }
    ],
    "lower": [{"template": '{ "r": lower($.t) }', "source": '{ "t": "ACME SA" }', "output": '{ "r": "acme sa" }'}],
    "padleft": [
        {
            "template": '{ "r": padleft($.t, 6, "0") }',
            "source": '{ "t": "42" }',
            "output": '{ "r": "000042" }',
        }
    ],
    "padright": [
        {
            "template": '{ "r": padright($.t, 6, ".") }',
            "source": '{ "t": "42" }',
            "output": '{ "r": "42...." }',
        }
    ],
    "repeat": [{"template": '{ "r": repeat($.t, 3) }', "source": '{ "t": "ab" }', "output": '{ "r": "ababab" }'}],
    "replace": [
        {
            "template": '{ "r": replace($.t, "-", "/") }',
            "source": '{ "t": "2026-11-11" }',
            "output": '{ "r": "2026/11/11" }',
        }
    ],
    "shorten": [
        {
            "template": '{ "r": shorten($.t, 12) }',
            "source": '{ "t": "Facture annuelle 2026" }',
            "output": '{ "r": "Facture…" }',
        }
    ],
    "split": [
        {
            "template": '{ "r": split($.t, ";") }',
            "source": '{ "t": "a;b;c" }',
            "output": '{ "r": ["a", "b", "c"] }',
        }
    ],
    "splitstring": [
        {
            "note": "Un séparateur **entier**, là où `split` ne garde que son 1er caractère.",
            "note_en": "A **whole** separator, where `split` only keeps its 1st character.",
            "template": '{ "entier": splitstring($.t, " - "), "premier_caractere": split($.t, " - ") }',
            "source": '{ "t": "a - b - c" }',
            "output": '{ "entier": ["a", "b", "c"], "premier_caractere": ["a", "-", "b", "-", "c"] }',
        },
        {
            "note": (
                "`limit` compte les **coupes** : `1` rend deux éléments, le reste du texte "
                "étant gardé entier."
            ),
            "note_en": (
                "`limit` counts the **cuts**: `1` returns two elements, the rest of the text "
                "being kept whole."
            ),
            "template": '{ "une_coupe": splitstring($.t, ",", 1) }',
            "source": '{ "t": "a,b,c" }',
            "output": '{ "une_coupe": ["a", "b,c"] }',
        },
    ],
    "startswith": [
        {
            "template": '{ "r": startswith($.t, "FR") }',
            "source": '{ "t": "FR7630006000011234567890189" }',
            "output": '{ "r": true }',
        }
    ],
    "stringcontains": [
        {
            "template": '{ "r": stringcontains($.t, "@") }',
            "source": '{ "t": "ana@exemple.fr" }',
            "output": '{ "r": true }',
        }
    ],
    "stringlenght": [
        {
            "template": '{ "r": stringlenght($.t) }',
            "source": '{ "t": "bonjour" }',
            "output": '{ "r": 7 }',
        }
    ],
    "substring": [
        {
            "template": '{ "debut": substring($.t, 0, 3), "depuis_la_fin": substring($.t, -2) }',
            "source": '{ "t": "bonjour" }',
            "output": '{ "debut": "bon", "depuis_la_fin": "ur" }',
        }
    ],
    "titlecase": [
        {
            "template": '{ "r": titlecase($.t) }',
            "source": '{ "t": "ana de la tour" }',
            "output": '{ "r": "Ana De La Tour" }',
        }
    ],
    "trim": [
        {
            "template": '{ "espaces": trim($.a), "caracteres": trim($.b, "*") }',
            "source": '{ "a": "  ok  ", "b": "**ok**" }',
            "output": '{ "espaces": "ok", "caracteres": "ok" }',
        }
    ],
    "trimend": [{"template": '{ "r": trimend($.t) }', "source": '{ "t": "ok   " }', "output": '{ "r": "ok" }'}],
    "trimstart": [{"template": '{ "r": trimstart($.t) }', "source": '{ "t": "   ok" }', "output": '{ "r": "ok" }'}],
    "upper": [{"template": '{ "r": upper($.t) }', "source": '{ "t": "acme" }', "output": '{ "r": "ACME" }'}],
    # --- pliage Unicode et proximité -------------------------------------------
    "deaccent": [
        {
            "template": '{ "r": deaccent($.t) }',
            "source": '{ "t": "Évêché" }',
            "output": '{ "r": "Eveche" }',
        }
    ],
    "foldtext": [
        {
            "template": '{ "r": foldtext($.t) }',
            "source": '{ "t": "Évêché" }',
            "output": '{ "r": "eveche" }',
        }
    ],
    "normalize": [
        {
            "template": '{ "r": stringlenght(normalize($.t, "C")) }',
            "source": '{ "t": "e\u0301" }',
            "output": '{ "r": 1 }',
        }
    ],
    "slugify": [
        {
            "template": '{ "r": slugify($.t) }',
            "source": '{ "t": "Évêché de Lyon" }',
            "output": '{ "r": "eveche-de-lyon" }',
        }
    ],
    "levenshtein": [
        {
            "template": '{ "r": levenshtein($.a, $.b) }',
            "source": '{ "a": "chat", "b": "chats" }',
            "output": '{ "r": 1 }',
        }
    ],
    "similarity": [
        {
            "template": '{ "r": round(similarity($.a, $.b), 2) }',
            "source": '{ "a": "Durand", "b": "Durrand" }',
            "output": '{ "r": 0.86 }',
        }
    ],
    # --- expressions régulières -------------------------------------------------
    "regexismatch": [
        {
            "template": '{ "r": regexismatch($.t, "^[A-Z]{2}[0-9]+$") }',
            "source": '{ "t": "FR123" }',
            "output": '{ "r": true }',
        }
    ],
    "regexmatches": [
        {
            "template": '{ "r": regexmatches($.t, "[0-9]+") }',
            "source": '{ "t": "a1 b22 c333" }',
            "output": '{ "r": ["1", "22", "333"] }',
        }
    ],
    "regexreplace": [
        {
            "template": '{ "r": regexreplace($.t, "(\\\\d{4})-(\\\\d{2})", "$2/$1") }',
            "source": '{ "t": "2026-11" }',
            "output": '{ "r": "11/2026" }',
        }
    ],
    "splitregex": [
        {
            "template": '{ "r": splitregex($.t, "\\\\s*;\\\\s*") }',
            "source": '{ "t": "a ; b;c" }',
            "output": '{ "r": ["a", "b", "c"] }',
        }
    ],
    # --- encodage et empreintes --------------------------------------------------
    "crc32": [{"template": '{ "r": crc32($.t) }', "source": '{ "t": "abc" }', "output": '{ "r": 891568578 }'}],
    "frombase64": [
        {
            "template": '{ "r": frombase64($.t) }',
            "source": '{ "t": "Ym9uam91cg==" }',
            "output": '{ "r": "bonjour" }',
        }
    ],
    "hexdecode": [
        {
            "template": '{ "r": hexdecode($.t) }',
            "source": '{ "t": "616263" }',
            "output": '{ "r": "abc" }',
        }
    ],
    "hexencode": [{"template": '{ "r": hexencode($.t) }', "source": '{ "t": "abc" }', "output": '{ "r": "616263" }'}],
    "hmacsha256": [
        {
            "template": '{ "r": hmacsha256($.t, $.cle) }',
            "source": '{ "t": "message", "cle": "secret" }',
            "output": '{ "r": "8b5f48702995c1598c573db1e21866a9b825d4a794d169d7060a03605796360b" }',
        }
    ],
    "htmlescape": [
        {
            "template": '{ "r": htmlescape($.t) }',
            "source": '{ "t": "<b>ok</b>" }',
            "output": '{ "r": "&lt;b&gt;ok&lt;/b&gt;" }',
        }
    ],
    "htmlunescape": [
        {
            "template": '{ "r": htmlunescape($.t) }',
            "source": '{ "t": "&lt;b&gt;ok&lt;/b&gt;" }',
            "output": '{ "r": "<b>ok</b>" }',
        }
    ],
    "md5": [
        {
            "template": '{ "r": md5($.t) }',
            "source": '{ "t": "abc" }',
            "output": '{ "r": "900150983cd24fb0d6963f7d28e17f72" }',
        }
    ],
    "sha1": [
        {
            "template": '{ "r": sha1($.t) }',
            "source": '{ "t": "abc" }',
            "output": '{ "r": "a9993e364706816aba3e25717850c26c9cd0d89d" }',
        }
    ],
    "sha256": [
        {
            "template": '{ "r": sha256($.t) }',
            "source": '{ "t": "abc" }',
            "output": '{ "r": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad" }',
        }
    ],
    "sha512": [
        {
            "template": '{ "r": stringlenght(sha512($.t)) }',
            "source": '{ "t": "abc" }',
            "output": '{ "r": 128 }',
        }
    ],
    "tobase64": [
        {
            "template": '{ "r": tobase64($.t) }',
            "source": '{ "t": "bonjour" }',
            "output": '{ "r": "Ym9uam91cg==" }',
        }
    ],
    "urldecode": [
        {
            "template": '{ "r": urldecode($.t) }',
            "source": '{ "t": "caf%C3%A9%20noir" }',
            "output": '{ "r": "café noir" }',
        }
    ],
    "urlencode": [
        {
            "template": '{ "r": urlencode($.t) }',
            "source": '{ "t": "café noir" }',
            "output": '{ "r": "caf%C3%A9%20noir" }',
        }
    ],
    # --- collections ------------------------------------------------------------
    "any": [
        {
            "template": '{ "pleine": any($.l), "vide": any($.v) }',
            "source": '{ "l": [1], "v": [] }',
            "output": '{ "pleine": true, "vide": false }',
        }
    ],
    "chunk": [
        {
            "template": '{ "r": chunk($.l, 2) }',
            "source": '{ "l": [1, 2, 3, 4, 5] }',
            "output": '{ "r": [[1, 2], [3, 4], [5]] }',
        }
    ],
    "concat": [
        {
            "template": '{ "colle": concat($.l), "joint": concat($.l, "-") }',
            "source": '{ "l": ["a", "b", "c"] }',
            "output": '{ "colle": "abc", "joint": "a-b-c" }',
        }
    ],
    "contains": [
        {
            "template": '{ "r": contains($.l, "b") }',
            "source": '{ "l": ["a", "b"] }',
            "output": '{ "r": true }',
        }
    ],
    "difference": [
        {
            "template": '{ "r": difference($.a, $.b) }',
            "source": '{ "a": [1, 2, 3], "b": [2] }',
            "output": '{ "r": [1, 3] }',
        }
    ],
    "distinct": [
        {
            "template": '{ "r": distinct($.l, $.*) }',
            "source": '{ "l": [1, 2, 2, 3] }',
            "output": '{ "r": [1, 2, 3] }',
        }
    ],
    "distinctby": [
        {
            "template": '{ "r": distinctby($.l, $.ville) }',
            "source": '{ "l": [{ "id": 1, "ville": "Lyon" }, { "id": 2, "ville": "Lyon" }, { "id": 3, "ville": "Brest" }] }',
            "output": '{ "r": [{ "id": 1, "ville": "Lyon" }, { "id": 3, "ville": "Brest" }] }',
        }
    ],
    "flatten": [
        {
            "template": '{ "a_fond": flatten($.l), "un_niveau": flatten($.l, 1) }',
            "source": '{ "l": [1, [2, [3]]] }',
            "output": '{ "a_fond": [1, 2, 3], "un_niveau": [1, 2, [3]] }',
        }
    ],
    "intersect": [
        {
            "template": '{ "r": intersect($.a, $.b) }',
            "source": '{ "a": [1, 2, 3], "b": [3, 1] }',
            "output": '{ "r": [1, 3] }',
        }
    ],
    "limit": [
        {
            "template": '{ "r": limit($.l, 2) }',
            "source": '{ "l": [1, 2, 3, 4] }',
            "output": '{ "r": [1, 2] }',
        }
    ],
    "partition": [
        {
            "template": '{ "r": partition($.l, $.actif) }',
            "source": '{ "l": [{ "n": "a", "actif": true }, { "n": "b", "actif": false }] }',
            "output": '{ "r": { "true": [{ "n": "a", "actif": true }], "false": [{ "n": "b", "actif": false }] } }',
        }
    ],
    "select": [
        {
            "template": '{ "r": select($.d, $.client.nom) }',
            "source": '{ "d": { "client": { "nom": "Ana" } } }',
            "output": '{ "r": "Ana" }',
        }
    ],
    "selectany": [
        {
            "template": '{ "r": selectany($.d, $.client.nom) }',
            "source": '{ "d": { "client": { "nom": "Ana" } } }',
            "output": '{ "r": true }',
        }
    ],
    "selectmany": [
        {
            "template": '{ "r": selectmany($.l, $.*.id) }',
            "source": '{ "l": [{ "id": 1 }, { "id": 2 }] }',
            "output": '{ "r": [1, 2] }',
        }
    ],
    "skip": [
        {
            "template": '{ "r": skip($.l, 2) }',
            "source": '{ "l": [1, 2, 3, 4] }',
            "output": '{ "r": [3, 4] }',
        }
    ],
    "union": [
        {
            "template": '{ "r": union($.l) }',
            "source": '{ "l": [[1, 2], [3]] }',
            "output": '{ "r": [1, 2, 3] }',
        }
    ],
    "unzip": [
        {
            "template": '{ "r": unzip($.l) }',
            "source": '{ "l": [[1, "a"], [2, "b"]] }',
            "output": '{ "r": [[1, 2], ["a", "b"]] }',
        }
    ],
    "window": [
        {
            "template": '{ "r": window($.l, 2) }',
            "source": '{ "l": [1, 2, 3] }',
            "output": '{ "r": [[1, 2], [2, 3]] }',
        }
    ],
    "zip": [
        {
            "template": '{ "r": zip($.a, $.b) }',
            "source": '{ "a": [1, 2], "b": ["x", "y"] }',
            "output": '{ "r": [[1, "x"], [2, "y"]] }',
        }
    ],
    # --- tri et ordre -------------------------------------------------------------
    "first": [{"template": '{ "r": first($.l) }', "source": '{ "l": [3, 1] }', "output": '{ "r": 3 }'}],
    "last": [{"template": '{ "r": last($.l) }', "source": '{ "l": [3, 1] }', "output": '{ "r": 1 }'}],
    "reverse": [
        {
            "template": '{ "tableau": reverse($.l), "texte": reverse($.t) }',
            "source": '{ "l": [1, 2, 3], "t": "abc" }',
            "output": '{ "tableau": [3, 2, 1], "texte": "cba" }',
        }
    ],
    "sort": [
        {
            "template": '{ "par_prix": selectmany(sort($.l, $.prix), $.*.id) }',
            "source": '{ "l": [{ "id": 1, "prix": 30 }, { "id": 2, "prix": 10 }] }',
            "output": '{ "par_prix": [2, 1] }',
        },
        {
            "template": '{ "ville_puis_prix_decroissant": selectmany(sort($.l, [$.ville, $.prix], [false, true]), $.*.id) }',
            "source": '{ "l": [{ "id": 1, "ville": "Lyon", "prix": 10 }, { "id": 2, "ville": "Lyon", "prix": 30 }, { "id": 3, "ville": "Brest", "prix": 5 }] }',
            "output": '{ "ville_puis_prix_decroissant": [3, 2, 1] }',
        },
    ],
    # --- agrégats et statistiques ---------------------------------------------------
    "avg": [{"template": '{ "r": avg($.n) }', "source": '{ "n": [1, 2, 6] }', "output": '{ "r": 3.0 }'}],
    "count": [
        {
            "template": '{ "tableau": count($.l), "objet": count($.o), "texte": count($.t) }',
            "source": '{ "l": [1, 2], "o": { "a": 1 }, "t": "abc" }',
            "output": '{ "tableau": 2, "objet": 1, "texte": 3 }',
        }
    ],
    "median": [{"template": '{ "r": median($.n) }', "source": '{ "n": [1, 9, 2] }', "output": '{ "r": 2 }'}],
    "mode": [
        {
            "template": '{ "r": mode($.l) }',
            "source": '{ "l": ["a", "b", "a"] }',
            "output": '{ "r": "a" }',
        }
    ],
    "percentile": [
        {
            "template": '{ "p90": percentile($.n, 90) }',
            "source": '{ "n": [1, 2, 3, 4, 5] }',
            "output": '{ "p90": 4.6 }',
        }
    ],
    "product": [{"template": '{ "r": product($.n) }', "source": '{ "n": [2, 3, 4] }', "output": '{ "r": 24 }'}],
    "stddev": [
        {
            "template": '{ "population": stddev($.n), "echantillon": round(stddev($.n, true), 3) }',
            "source": '{ "n": [2, 4, 4, 4, 5, 5, 7, 9] }',
            "output": '{ "population": 2.0, "echantillon": 2.138 }',
        }
    ],
    "sum": [{"template": '{ "r": sum($.n) }', "source": '{ "n": [1, 2, 3] }', "output": '{ "r": 6 }'}],
    "variance": [
        {
            "template": '{ "r": variance($.n) }',
            "source": '{ "n": [2, 4, 4, 4, 5, 5, 7, 9] }',
            "output": '{ "r": 4.0 }',
        }
    ],
    # --- agrégation par clef calculée ------------------------------------------------
    "avgby": [
        {
            "template": '{ "r": avgby($.l, $.ville, $.m) }',
            "source": '{ "l": [{ "ville": "Lyon", "m": 10 }, { "ville": "Lyon", "m": 20 }, { "ville": "Brest", "m": 7 }] }',
            "output": '{ "r": { "Lyon": 15.0, "Brest": 7.0 } }',
        }
    ],
    "countby": [
        {
            "template": '{ "r": countby($.l, $.ville) }',
            "source": '{ "l": [{ "ville": "Lyon" }, { "ville": "Lyon" }, { "ville": "Brest" }] }',
            "output": '{ "r": { "Lyon": 2, "Brest": 1 } }',
        }
    ],
    "groupby": [
        {
            "template": '{ "plat": groupby($.l, $.ville) }',
            "source": '{ "l": [{ "id": 1, "ville": "Lyon" }, { "id": 2, "ville": "Brest" }] }',
            "output": '{ "plat": { "Lyon": [{ "id": 1, "ville": "Lyon" }], "Brest": [{ "id": 2, "ville": "Brest" }] } }',
        },
        {
            "template": '{ "imbrique": groupby($.l, [$.pays, $.ville], true) }',
            "source": '{ "l": [{ "id": 1, "pays": "FR", "ville": "Lyon" }] }',
            "output": '{ "imbrique": { "FR": { "Lyon": [{ "id": 1, "pays": "FR", "ville": "Lyon" }] } } }',
        },
    ],
    "sumby": [
        {
            "template": '{ "r": sumby($.l, $.ville, $.m) }',
            "source": '{ "l": [{ "ville": "Lyon", "m": 10 }, { "ville": "Lyon", "m": 5 }, { "ville": "Brest", "m": 7 }] }',
            "output": '{ "r": { "Lyon": 15, "Brest": 7 } }',
        }
    ],
    # --- regroupement et jointure ------------------------------------------------------
    "group": [
        {
            "template": '{ "r": group($.p, ["$.ville"]) }',
            "source": '{ "p": [{ "nom": "Ana", "ville": "Lyon" }] }',
            "output": '{ "r": [{ "Label": "Lyon", "Items": [{ "nom": "Ana", "ville": "Lyon" }] }] }',
        }
    ],
    "join": [
        {
            "template": '{ "r": join($.c, $.id, false, [{ "Name": "commandes", "Key": "$.client", "Source": $.o }]) }',
            "source": '{ "c": [{ "id": 1, "nom": "Ana" }], "o": [{ "client": 1, "total": 12 }] }',
            "output": '{ "r": [{ "id": 1, "nom": "Ana", "commandes": [{ "total": 12 }] }] }',
        }
    ],
    "createindex": [
        {
            "template": '{ "i:": createindex($.p, "", "$.nom"), "ana": index(i:, "Ana") }',
            "source": '{ "p": [{ "nom": "Ana", "ville": "Lyon" }] }',
            "output": '{ "ana": { "nom": "Ana", "ville": "Lyon" } }',
        }
    ],
    "index": [
        {
            "template": '{ "i:": createindex($.p, "", "$.nom"), "ana": index(i:, "Ana") }',
            "source": '{ "p": [{ "nom": "Ana", "ville": "Lyon" }] }',
            "output": '{ "ana": { "nom": "Ana", "ville": "Lyon" } }',
        }
    ],
    # --- types et repli ----------------------------------------------------------------
    "convert": [
        {
            "template": '{ "entier": convert($.t, "integer"), "texte": convert($.n, "string") }',
            "source": '{ "t": "42", "n": 7 }',
            "output": '{ "entier": 42, "texte": "7" }',
        }
    ],
    "isarray": [
        {
            "template": '{ "tableau": isarray($.l), "objet": isarray($.o) }',
            "source": '{ "l": [], "o": {} }',
            "output": '{ "tableau": true, "objet": false }',
        }
    ],
    "isboolean": [
        {
            "template": '{ "r": isboolean($.b), "nombre": isboolean($.n) }',
            "source": '{ "b": false, "n": 0 }',
            "output": '{ "r": true, "nombre": false }',
        }
    ],
    "isnotnull": [
        {
            "template": '{ "presente": isnotnull($.a), "absente": isnotnull($.z) }',
            "source": '{ "a": 0 }',
            "output": '{ "presente": true, "absente": false }',
        }
    ],
    "isnull": [
        {
            "template": '{ "absente": isnull($.z), "vide": isnull($.t) }',
            "source": '{ "t": "" }',
            "output": '{ "absente": true, "vide": false }',
        }
    ],
    "isnumber": [
        {
            "template": '{ "nombre": isnumber($.n), "booleen": isnumber($.b) }',
            "source": '{ "n": 3, "b": true }',
            "output": '{ "nombre": true, "booleen": false }',
        }
    ],
    "isobject": [
        {
            "template": '{ "objet": isobject($.o), "tableau": isobject($.l) }',
            "source": '{ "o": {}, "l": [] }',
            "output": '{ "objet": true, "tableau": false }',
        }
    ],
    "isstring": [
        {
            "template": '{ "texte": isstring($.t), "nombre": isstring($.n) }',
            "source": '{ "t": "a", "n": 1 }',
            "output": '{ "texte": true, "nombre": false }',
        }
    ],
    "parsejson": [
        {
            "template": '{ "r": select(parsejson($.t), $.ville) }',
            "source": '{ "t": "{\\"ville\\": \\"Lyon\\"}" }',
            "output": '{ "r": "Lyon" }',
        }
    ],
    "trydefault": [
        {
            "template": '{ "r": trydefault($.a / $.b, "division impossible") }',
            "source": '{ "a": 1, "b": 0 }',
            "output": '{ "r": "division impossible" }',
        }
    ],
    "typeof": [
        {
            "template": '{ "texte": typeof($.t), "tableau": typeof($.l), "absent": typeof($.z) }',
            "source": '{ "t": "a", "l": [] }',
            "output": '{ "texte": "string", "tableau": "array", "absent": "null" }',
        }
    ],
    # --- objets ---------------------------------------------------------------------
    "entries": [
        {
            "template": '{ "r": entries($.o) }',
            "source": '{ "o": { "a": 1, "b": 2 } }',
            "output": '{ "r": [{ "key": "a", "value": 1 }, { "key": "b", "value": 2 }] }',
        }
    ],
    "fromentries": [
        {
            "template": '{ "r": fromentries($.l) }',
            "source": '{ "l": [{ "key": "a", "value": 1 }] }',
            "output": '{ "r": { "a": 1 } }',
        }
    ],
    "has": [
        {
            "template": '{ "presente": has($.o, "a"), "absente": has($.o, "z") }',
            "source": '{ "o": { "a": null } }',
            "output": '{ "presente": true, "absente": false }',
        }
    ],
    "keys": [{"template": '{ "r": keys($.o) }', "source": '{ "o": { "a": 1, "b": 2 } }', "output": '{ "r": ["a", "b"] }'}],
    "merge": [
        {
            "template": '{ "r": merge($.a, $.b) }',
            "source": '{ "a": { "x": 1, "y": 2 }, "b": { "y": 9 } }',
            "output": '{ "r": { "x": 1, "y": 9 } }',
        }
    ],
    "omit": [
        {
            "template": '{ "r": omit($.o, ["secret"]) }',
            "source": '{ "o": { "nom": "Ana", "secret": "x" } }',
            "output": '{ "r": { "nom": "Ana" } }',
        }
    ],
    "pick": [
        {
            "template": '{ "r": pick($.o, ["nom", "ville"]) }',
            "source": '{ "o": { "nom": "Ana", "ville": "Lyon", "secret": "x" } }',
            "output": '{ "r": { "nom": "Ana", "ville": "Lyon" } }',
        }
    ],
    "renamekeys": [
        {
            "template": '{ "r": renamekeys($.o, { "nom": "name" }) }',
            "source": '{ "o": { "nom": "Ana", "ville": "Lyon" } }',
            "output": '{ "r": { "name": "Ana", "ville": "Lyon" } }',
        }
    ],
    "values": [{"template": '{ "r": values($.o) }', "source": '{ "o": { "a": 1, "b": 2 } }', "output": '{ "r": [1, 2] }'}],
    # --- structures profondes ----------------------------------------------------------
    "flattenobject": [
        {
            "template": '{ "r": flattenobject($.o) }',
            "source": '{ "o": { "client": { "nom": "Ana" } } }',
            "output": '{ "r": { "client.nom": "Ana" } }',
        }
    ],
    "prune": [
        {
            "template": '{ "nulls": prune($.o), "vides_aussi": prune($.o, "empty") }',
            "source": '{ "o": { "a": 1, "b": null, "c": "" } }',
            "output": '{ "nulls": { "a": 1, "c": "" }, "vides_aussi": { "a": 1 } }',
        }
    ],
    "setpath": [
        {
            "template": '{ "r": setpath($.o, "client.ville", "Lyon") }',
            "source": '{ "o": { "client": { "nom": "Ana" } } }',
            "output": '{ "r": { "client": { "nom": "Ana", "ville": "Lyon" } } }',
        }
    ],
    "unflatten": [
        {
            "template": '{ "r": unflatten($.o) }',
            "source": '{ "o": { "client.nom": "Ana" } }',
            "output": '{ "r": { "client": { "nom": "Ana" } } }',
        }
    ],
    "unsetpath": [
        {
            "template": '{ "r": unsetpath($.o, "client.secret") }',
            "source": '{ "o": { "client": { "nom": "Ana", "secret": "x" } } }',
            "output": '{ "r": { "client": { "nom": "Ana" } } }',
        }
    ],
    "walk": [
        {
            "template": '{ "r": walk($.o, when(isstring($)) { "True": upper($), "default": $ }) }',
            "source": '{ "o": { "a": "x", "b": { "c": "y" } } }',
            "output": '{ "r": { "a": "X", "b": { "c": "Y" } } }',
        }
    ],
    # --- dates --------------------------------------------------------------------------
    "dateadd": [
        {
            "note": "Ajouter, et retrancher avec un nombre négatif.",
            "note_en": "Adding, and subtracting with a negative amount.",
            "template": '{ "dans_deux_mois": dateadd($.d, "month", 2), "hier": dateadd($.d, "day", -1) }',
            "source": '{ "d": "2026-01-15T00:00:00" }',
            "output": '{ "dans_deux_mois": "2026-03-15T00:00:00", "hier": "2026-01-14T00:00:00" }',
        },
        {
            "note": (
                "`month` est **calendaire** : le 31 janvier + 1 mois donne le 28 février, "
                "borné sur le mois court — et non le 3 mars."
            ),
            "note_en": (
                "`month` is a **calendar** unit: 31 January + 1 month gives 28 February, "
                "clamped on the short month — not 3 March."
            ),
            "template": '{ "borne": dateadd($.d, "month", 1) }',
            "source": '{ "d": "2026-01-31T00:00:00" }',
            "output": '{ "borne": "2026-02-28T00:00:00" }',
        },
    ],
    "datediff": [
        {
            "note": "Des unités **entières** écoulées, négatives si la fin précède le début.",
            "note_en": "**Whole** elapsed units, negative when the end precedes the start.",
            "template": '{ "jours": datediff($.a, $.b, "day"), "a_rebours": datediff($.b, $.a, "day") }',
            "source": '{ "a": "2026-11-01T00:00:00", "b": "2026-11-11T00:00:00" }',
            "output": '{ "jours": 10, "a_rebours": -10 }',
        },
        {
            "note": (
                "Un mois n'est compté que lorsque le **jour** de la fin a rattrapé celui du "
                "début : du 15 janvier au 14 février, il y en a zéro."
            ),
            "note_en": (
                "A month only counts once the end's **day** has caught up with the start's: "
                "from 15 January to 14 February there is none."
            ),
            "template": '{ "veille": datediff($.a, $.b, "month"), "jour_meme": datediff($.a, $.c, "month") }',
            "source": '{ "a": "2026-01-15T00:00:00", "b": "2026-02-14T00:00:00", "c": "2026-02-15T00:00:00" }',
            "output": '{ "veille": 0, "jour_meme": 1 }',
        },
    ],
    "dateduration": [
        {
            "note": (
                "L'intervalle décomposé en valeurs **positives** ; `negative` dit dans quel "
                "sens il va."
            ),
            "note_en": (
                "The interval broken down into **positive** values; `negative` says which "
                "way it goes."
            ),
            "template": '{ "r": dateduration($.a, $.b) }',
            "source": '{ "a": "2026-01-01T00:00:00", "b": "2027-03-02T04:05:06" }',
            "output": '{ "r": { "negative": false, "years": 1, "months": 2, "days": 1, "hours": 4, "minutes": 5, "seconds": 6 } }',
        }
    ],
    "dateendof": [
        {
            "note": (
                "Borne **inclusive** : la dernière microseconde de la période, pour qu'un "
                "filtre `<=` attrape toute la journée (ou tout le mois)."
            ),
            "note_en": (
                "An **inclusive** bound: the last microsecond of the period, so that a `<=` "
                "filter catches the whole day (or the whole month)."
            ),
            "template": '{ "mois": dateendof($.d, "month"), "jour": dateendof($.d, "day") }',
            "source": '{ "d": "2026-02-10T12:00:00" }',
            "output": '{ "mois": "2026-02-28T23:59:59.999999", "jour": "2026-02-10T23:59:59.999999" }',
        }
    ],
    "datepart": [
        {
            "note": (
                "`dayofweek` compte à partir de **dimanche = 0** : le 11 novembre 2026 est "
                "un mercredi, donc 3."
            ),
            "note_en": (
                "`dayofweek` counts from **Sunday = 0**: 11 November 2026 is a Wednesday, "
                "hence 3."
            ),
            "template": '{ "annee": datepart($.d, "year"), "trimestre": datepart($.d, "quarter"), "jour_semaine": datepart($.d, "dayofweek") }',
            "source": '{ "d": "2026-11-11T09:30:00" }',
            "output": '{ "annee": 2026, "trimestre": 4, "jour_semaine": 3 }',
        }
    ],
    "datestartof": [
        {
            "note": (
                "La semaine commence **lundi** : un mercredi est ramené au lundi qui le "
                "précède, à minuit."
            ),
            "note_en": (
                "The week starts on **Monday**: a Wednesday is brought back to the Monday "
                "before it, at midnight."
            ),
            "template": '{ "semaine": datestartof($.d, "week"), "mois": datestartof($.d, "month") }',
            "source": '{ "d": "2026-11-11T09:30:00" }',
            "output": '{ "semaine": "2026-11-09T00:00:00", "mois": "2026-11-01T00:00:00" }',
        }
    ],
    "datesub": [
        {
            "template": '{ "r": datesub($.d, "day", 1) }',
            "source": '{ "d": "2026-03-01T00:00:00" }',
            "output": '{ "r": "2026-02-28T00:00:00" }',
        }
    ],
    "datezone": [
        {
            "note": (
                "Sur une date **sans** décalage, le fuseau est attribué : l'heure affichée "
                "ne bouge pas. Sur une date qui en porte un, elle est convertie : c'est "
                "l'**instant** qui ne bouge pas."
            ),
            "note_en": (
                "On a date **without** an offset, the timezone is attached: the displayed "
                "time does not move. On one that carries an offset, it is converted: this "
                "time the **instant** does not move."
            ),
            "template": '{ "attribue": datezone($.a, "Europe/Paris"), "converti": datezone($.b, "UTC") }',
            "source": '{ "a": "2026-11-11T09:30:00", "b": "2026-11-11T09:30:00+01:00" }',
            "output": '{ "attribue": "2026-11-11T09:30:00+01:00", "converti": "2026-11-11T08:30:00+00:00" }',
        }
    ],
    "now": [
        {
            "template": '{ "r": datepart(now(), "year") >= 2026 }',
            "source": "{}",
            "output": '{ "r": true }',
        }
    ],
    "parsedate": [
        {
            "note": "Une date **ISO 8601** se lit sans rien : ni culture, ni masque.",
            "note_en": "An **ISO 8601** date reads with nothing: no culture, no mask.",
            "template": '{ "d": parsedate($.t) }',
            "source": '{ "t": "2026-11-11T09:30:00Z" }',
            "output": '{ "d": "2026-11-11T09:30:00+00:00" }',
        },
        {
            "note": (
                "Sans masque, c'est la **culture** qui décide de l'ordre : mois d'abord en "
                "`en-US`, jour d'abord partout ailleurs. Le même texte donne deux dates."
            ),
            "note_en": (
                "With no mask, the **culture** decides the order: month first in `en-US`, "
                "day first everywhere else. The same text gives two dates."
            ),
            "template": '{ "us": parsedate($.t, "en-US"), "gb": parsedate($.t, "en-GB") }',
            "source": '{ "t": "03/04/2026" }',
            "output": '{ "us": "2026-03-04T00:00:00", "gb": "2026-04-03T00:00:00" }',
        },
        {
            "note": (
                "Un mois **en toutes lettres** exige un masque : la détection automatique ne "
                "lit que les formes numériques et l'ISO. `MMMM` prend les noms de la culture."
            ),
            "note_en": (
                "A month **spelled out** requires a mask: automatic detection only reads "
                "numeric forms and ISO. `MMMM` takes the culture's names."
            ),
            "template": '{ "en": parsedate($.a, "en-US", "MMMM d, yyyy"), "fr": parsedate($.b, "fr-FR", "d MMMM yyyy") }',
            "source": '{ "a": "November 11, 2026", "b": "11 novembre 2026" }',
            "output": '{ "en": "2026-11-11T00:00:00", "fr": "2026-11-11T00:00:00" }',
        },
        {
            "note": (
                "Abrégés (`MMM`, `ddd`), et heure sur 12 h : `h` **exige** `tt`, le "
                "désignateur AM/PM de la culture."
            ),
            "note_en": (
                "Abbreviations (`MMM`, `ddd`), and a 12-hour clock: `h` **requires** `tt`, "
                "the culture's AM/PM designator."
            ),
            "template": '{ "jour": parsedate($.a, "en-GB", "ddd, d MMM yyyy"), "heure": parsedate($.b, "en-US", "MM/dd/yyyy h:mm tt") }',
            "source": '{ "a": "Wed, 11 Nov 2026", "b": "11/11/2026 2:05 PM" }',
            "output": '{ "jour": "2026-11-11T00:00:00", "heure": "2026-11-11T14:05:00" }',
        },
        {
            "note": (
                "Sans séparateurs, un masque suffit. Et un masque d'**une seule lettre** est "
                "un masque standard, résolu selon la culture (`d` = date courte)."
            ),
            "note_en": (
                "Without separators, a mask is enough. And a **single-letter** mask is a "
                "standard mask, resolved per culture (`d` = short date)."
            ),
            "template": '{ "compact": parsedate($.a, "", "yyyyMMdd"), "court": parsedate($.b, "en-US", "d") }',
            "source": '{ "a": "20261111", "b": "11/11/2026" }',
            "output": '{ "compact": "2026-11-11T00:00:00", "court": "2026-11-11T00:00:00" }',
        },
        {
            "note": (
                "Une composante absente du masque vient de l'**époque Unix**, jamais "
                "d'aujourd'hui : le même template rend la même chose demain."
            ),
            "note_en": (
                "A component the mask does not carry comes from the **Unix epoch**, never "
                "from today: the same template returns the same thing tomorrow."
            ),
            "template": '{ "heure_seule": parsedate($.t, "", "HH:mm") }',
            "source": '{ "t": "11:30" }',
            "output": '{ "heure_seule": "1970-01-01T11:30:00" }',
        },
        {
            "note": (
                "Le 4e argument **qualifie** une date sans décalage (on lui donne un fuseau) "
                "et **convertit** une date qui en porte déjà un."
            ),
            "note_en": (
                "The 4th argument **qualifies** a date without offset (it is given a "
                "timezone) and **converts** one that already carries an offset."
            ),
            "template": '{ "qualifie": parsedate($.a, "", "", "Europe/Paris"), "convertit": parsedate($.b, "", "", "UTC") }',
            "source": '{ "a": "2026-11-11", "b": "2026-11-11T09:30:00+01:00" }',
            "output": '{ "qualifie": "2026-11-11T00:00:00+01:00", "convertit": "2026-11-11T08:30:00+00:00" }',
        },
    ],
    "today": [
        {
            "template": '{ "r": datepart(today(), "hour") }',
            "source": "{}",
            "output": '{ "r": 0 }',
        }
    ],
    # --- formatage -----------------------------------------------------------------------
    "format": [
        {
            "note": (
                "Masques de **nombre** : une lettre et une précision. La culture fournit les "
                "séparateurs et le symbole."
            ),
            "note_en": (
                "**Number** masks: a letter and a precision. The culture provides the "
                "separators and the symbol."
            ),
            "template": '{ "nombre": format($.n, "N2", "fr-FR"), "pourcent": format($.p, "P0", "fr-FR") }',
            "source": '{ "n": 1234.5, "p": 0.25 }',
            "output": '{ "nombre": "1 234,50", "pourcent": "25 %" }',
        },
        {
            "note": (
                "Masques de **date** : mêmes jetons qu'à la lecture, et les noms de jours et "
                "de mois viennent de la culture."
            ),
            "note_en": (
                "**Date** masks: the same tokens as for reading, and the day and month names "
                "come from the culture."
            ),
            "template": '{ "date": format($.d, "dd/MM/yyyy"), "long": format($.d, "dddd d MMMM yyyy", "fr-FR") }',
            "source": '{ "d": "2026-11-11T09:30:00" }',
            "output": '{ "date": "11/11/2026", "long": "mercredi 11 novembre 2026" }',
        },
    ],
    # --- schéma --------------------------------------------------------------------------
    "schema": [
        {
            "template": '{ "r": schema($.o) }',
            "source": '{ "o": { "nom": "Ana" } }',
            "output": '{ "r": { "$schema": "http://json-schema.org/draft-04/schema#", "type": "object", "properties": { "nom": { "type": "string" } } } }',
        }
    ],
    "schemaerrors": [
        {
            "template": '{ "r": schemaerrors($.o, $.s) }',
            "source": '{ "o": { "age": "vieux" }, "s": { "type": "object", "properties": { "age": { "type": "integer" } } } }',
            "output": '{ "r": ["$.age : attendu un entier, reçu une chaîne"] }',
        }
    ],
    "schemaisvalid": [
        {
            "template": '{ "r": schemaisvalid($.o, $.s) }',
            "source": '{ "o": { "age": 42 }, "s": { "type": "object", "properties": { "age": { "type": "integer" } } } }',
            "output": '{ "r": true }',
        }
    ],
    # --- qualité et diagnostic --------------------------------------------------------------
    "isemail": [
        {
            "template": '{ "r": isemail($.t) }',
            "source": '{ "t": "ana@exemple.fr" }',
            "output": '{ "r": true }',
        }
    ],
    "isiban": [
        {
            "template": '{ "r": isiban($.t) }',
            "source": '{ "t": "FR7630006000011234567890189" }',
            "output": '{ "r": true }',
        }
    ],
    "isurl": [
        {
            "template": '{ "r": isurl($.t) }',
            "source": '{ "t": "https://exemple.fr/a" }',
            "output": '{ "r": true }',
        }
    ],
    "isuuid": [
        {
            "template": '{ "r": isuuid(uuid()) }',
            "source": "{}",
            "output": '{ "r": true }',
        }
    ],
    "require": [
        {
            "template": '{ "r": require($.n, "le montant est obligatoire") }',
            "source": '{ "n": 0 }',
            "output": '{ "r": 0 }',
        }
    ],
    "requirethat": [
        {
            "template": '{ "r": trydefault(requirethat($.n > 100, "montant trop faible"), "refusé") }',
            "source": '{ "n": 10 }',
            "output": '{ "r": "refusé" }',
        }
    ],
    "trace": [
        {
            "template": '{ "r": trace($.n, "montant") }',
            "source": '{ "n": 42 }',
            "output": '{ "r": 42 }',
        }
    ],
    "traces": [
        {
            "template": '{ "r": trace($.n, "montant"), "journal": traces() }',
            "source": '{ "n": 42 }',
            "output": '{ "r": 42, "journal": [{ "label": "montant", "value": 42 }] }',
        }
    ],
    # --- divers ----------------------------------------------------------------------------
    "param": [
        {
            "template": '{ "r": param("lot", "defaut") }',
            "source": "{}",
            "output": '{ "r": "defaut" }',
        }
    ],
    "params": [
        {
            "template": '{ "r": params() }',
            "source": "{}",
            "output": '{ "r": {} }',
        }
    ],
    "uuid": [
        {
            "template": '{ "r": stringlenght(uuid()) }',
            "source": "{}",
            "output": '{ "r": 36 }',
        }
    ],
    # --- sortie texte ---------------------------------------------------------------------
    # Ces cinq-là ne s'appellent pas dans le corps du template : le triplet montre
    # ce que rend `transform()` (la directive n'y paraît jamais), et `render` le
    # texte produit — vérifié lui aussi par la suite.
    "to_block": [
        {
            "template": '{ "$directives": { "output": { "filter": $.lignes, "mode": to_block() } }, "lignes": $.l[*] }',
            "source": '{ "l": [{ "id": 1 }, { "id": 2 }] }',
            "output": '{ "lignes": [{ "id": 1 }, { "id": 2 }] }',
            "render": '{"id":1}\n{"id":2}\n',
        }
    ],
    "to_csv": [
        {
            "template": '{ "$directives": { "output": { "filter": $.lignes, "mode": to_csv() } }, "lignes": [ { "$source": $.clients, "id": $.id, "ville": $.adr.ville } ] }',
            "source": '{ "clients": [{ "id": 1, "adr": { "ville": "Lyon" } }] }',
            "output": '{ "lignes": [{ "id": 1, "ville": "Lyon" }] }',
            "render": "id;ville\r\n1;Lyon\r\n",
        }
    ],
    "to_json": [
        {
            "template": '{ "$directives": { "output": { "mode": to_json(true) } }, "ville": $.v }',
            "source": '{ "v": "Lyon" }',
            "output": '{ "ville": "Lyon" }',
            "render": '{\n  "ville": "Lyon"\n}\n',
        }
    ],
    "to_xml": [
        {
            "template": '{ "$directives": { "output": { "filter": $.client, "mode": to_xml("client") } }, "client": { "@id": $.id, "ville": $.v } }',
            "source": '{ "id": 1, "v": "Lyon" }',
            "output": '{ "client": { "@id": 1, "ville": "Lyon" } }',
            "render": '<?xml version="1.0" encoding="utf-8"?>\n<client id="1"><ville>Lyon</ville></client>\n',
        }
    ],
    "to_yaml": [
        {
            "template": '{ "$directives": { "output": { "filter": $.client, "mode": to_yaml() } }, "client": { "id": $.id, "ville": $.v } }',
            "source": '{ "id": 1, "v": "Lyon" }',
            "output": '{ "client": { "id": 1, "ville": "Lyon" } }',
            "render": "id: 1\nville: Lyon\n",
        }
    ],
    # --- conditionnelle, accès calculé, arrondis ---------------------------------------
    "ifelse": [
        {
            "note": "La branche écartée n'est **pas** évaluée : la division par zéro ne part pas.",
            "note_en": "The branch left aside is **not** evaluated: the division by zero does not run.",
            "template": '{ "taille": ifelse($.n > 10, "grand", "petit"), "ratio": ifelse($.d == 0, 0, 100 / $.d) }',
            "source": '{ "n": 42, "d": 0 }',
            "output": '{ "taille": "grand", "ratio": 0 }',
        }
    ],
    "get": [
        {
            "note": "La clef vient des **données** : un chemin, lui, est écrit dans le template.",
            "note_en": "The key comes from the **data**: a path, by contrast, is written in the template.",
            "template": '{ "r": get($.o, $.k), "dernier": get($.l, -1) }',
            "source": '{ "o": { "a": 1, "b": 2 }, "k": "b", "l": [7, 8, 9] }',
            "output": '{ "r": 2, "dernier": 9 }',
        }
    ],
    "getpath": [
        {
            "template": '{ "r": getpath($.o, $.champ) }',
            "source": '{ "o": { "client": { "ville": "Lyon" } }, "champ": "client.ville" }',
            "output": '{ "r": "Lyon" }',
        }
    ],
    "roundhalfup": [
        {
            "note": "`round($.n, 2)` rendrait `0.12` : il arrondit le demi vers le **pair**.",
            "note_en": "`round($.n, 2)` would give `0.12`: it rounds the half to the **even** digit.",
            "template": '{ "commercial": roundhalfup($.n, 2), "bancaire": round($.n, 2) }',
            "source": '{ "n": 0.125 }',
            "output": '{ "commercial": 0.13, "bancaire": 0.12 }',
        }
    ],
    "roundto": [
        {
            "template": '{ "caisse": roundto($.n, 0.05), "quart_heure": roundto($.m, 15) }',
            "source": '{ "n": 2.34, "m": 38 }',
            "output": '{ "caisse": 2.35, "quart_heure": 45.0 }',
        }
    ],
    "toprecision": [
        {
            "note": "Trois chiffres significatifs, quel que soit l'ordre de grandeur.",
            "note_en": "Three significant digits, whatever the order of magnitude.",
            "template": '{ "grand": toprecision($.a, 3), "petit": toprecision($.b, 3) }',
            "source": '{ "a": 1234.5, "b": 0.00241348 }',
            "output": '{ "grand": 1230.0, "petit": 0.00241 }',
        }
    ],
    "stringlength": [
        {
            "note": "Même fonction que `stringlenght`, dont l'orthographe d'origine est fautive.",
            "note_en": "The same function as `stringlenght`, whose original spelling is a typo.",
            "template": '{ "r": stringlength($.t) }',
            "source": '{ "t": "Ana" }',
            "output": '{ "r": 3 }',
        }
    ],
}
