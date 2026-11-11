<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# Référence des fonctions

*Français · [English](sommaire.en.md)*

Une page par fonction, engendrée depuis le registre : signature, arguments et description. La prose et les exemples vivent dans les chapitres du guide.

## [Dates et heures](../dates.md)

| Fonction | Description |
|---|---|
| [`dateadd`](dateadd.md) | Ajoute une durée à une date ISO 8601 : unité second, minute, hour, day, week, month ou year, et un nombre entier (négatif pour retrancher) |
| [`datediff`](datediff.md) | Compte les unités entières écoulées entre deux dates ISO 8601 : second, minute, hour, day, week, month ou year, négatif si la fin précède le début |
| [`dateduration`](dateduration.md) | Décompose l'intervalle entre deux dates en années, mois, jours, heures, minutes et secondes |
| [`dateendof`](dateendof.md) | Dernier instant de la période contenant la date (borne inclusive, à la microseconde près) |
| [`datepart`](datepart.md) | Extrait une composante entière d'une date ISO 8601 : year, month, day, dayofweek (dimanche = 0), hour, minute ou second |
| [`datestartof`](datestartof.md) | Premier instant de la période contenant la date : year, quarter, month, week (lundi), day, hour ou minute |
| [`datesub`](datesub.md) | Retranche une durée à une date ISO 8601 : unité second, minute, hour, day, week, month ou year, et un nombre entier |
| [`datezone`](datezone.md) | Attribue un fuseau à une date sans décalage, ou convertit une date qui en porte déjà un |
| [`now`](now.md) | Date et heure courantes en ISO 8601 : locales, ou UTC si utc vaut true |
| [`parsedate`](parsedate.md) | Lit une date texte et la rend en ISO 8601 : détection selon la culture, ou masque explicite (dd/MM/yyyy…), avec un fuseau optionnel |
| [`today`](today.md) | Date du jour à minuit en ISO 8601 : locale, ou UTC si utc vaut true |

## [Données et collections](../collections.md)

| Fonction | Description |
|---|---|
| [`any`](any.md) | Vrai si la source est un tableau non vide |
| [`avg`](avg.md) | Moyenne des nombres d'un tableau (null pour un tableau vide) |
| [`avgby`](avgby.md) | Moyenne par clef calculée, en un objet { clef: moyenne } (la valeur par défaut est l'élément) |
| [`chunk`](chunk.md) | Découpe un tableau en tranches consécutives de size éléments |
| [`concat`](concat.md) | Joint les éléments d'un tableau en un texte, séparés par split_char suivi de delimit_char |
| [`contains`](contains.md) | Vrai si le tableau contient un élément égal à la valeur |
| [`convert`](convert.md) | Convertit une valeur vers un type : integer, decimal, string, boolean (uri, uuid, datetime, time en texte) |
| [`count`](count.md) | Nombre d'éléments : éléments d'un tableau, clés d'un objet, caractères d'un texte, 0 pour null |
| [`countby`](countby.md) | Compte les éléments d'un tableau par clef calculée, en un objet { clef: nombre } |
| [`createindex`](createindex.md) | Construit un index {clé: élément} à partir d'une source, d'un chemin de découpe et d'un chemin de clé |
| [`difference`](difference.md) | Éléments du tableau de gauche absents du tableau de droite, dédupliqués |
| [`distinct`](distinct.md) | Valeurs uniques sélectionnées par un chemin JSONPath dans un tableau, dans l'ordre d'apparition |
| [`distinctby`](distinctby.md) | Déduplique un tableau sur une clef calculée par élément, en gardant le premier |
| [`first`](first.md) | Premier élément d'un tableau, ou null s'il est vide |
| [`flatten`](flatten.md) | Aplatit un tableau de tableaux, à fond par défaut ou sur depth niveaux |
| [`group`](group.md) | Regroupe un tableau par chemins JSONPath successifs en {Label, Items} imbriqués |
| [`groupby`](groupby.md) | Regroupe un tableau en un objet { clef: éléments }, clef calculée par élément ; nested imbrique un niveau par clef d'un tableau de clefs |
| [`index`](index.md) | Élément d'un index (créé par createindex) pour une clé, ou null |
| [`intersect`](intersect.md) | Éléments du tableau de gauche présents aussi à droite, dédupliqués |
| [`join`](join.md) | Jointure gauche : rattache aux objets de gauche les éléments de droite de même clé |
| [`last`](last.md) | Dernier élément d'un tableau, ou null s'il est vide |
| [`limit`](limit.md) | Les max_items premiers éléments d'un tableau |
| [`median`](median.md) | Valeur médiane des nombres d'un tableau (null pour un tableau vide) |
| [`mode`](mode.md) | Valeur la plus fréquente d'un tableau (la première apparue en cas d'égalité) |
| [`partition`](partition.md) | Sépare un tableau en { true, false } selon un prédicat évalué par élément |
| [`percentile`](percentile.md) | Centile p (0 à 100) des nombres d'un tableau, par interpolation linéaire |
| [`product`](product.md) | Produit des nombres d'un tableau (1 pour un tableau vide) |
| [`reverse`](reverse.md) | Inverse l'ordre d'un tableau ou d'un texte, sans modifier la source |
| [`select`](select.md) | Première valeur sélectionnée par un chemin JSONPath dans la source, ou null |
| [`selectany`](selectany.md) | Vrai si le chemin JSONPath sélectionne au moins une valeur dans la source |
| [`selectmany`](selectmany.md) | Toutes les valeurs sélectionnées par un chemin JSONPath dans la source |
| [`skip`](skip.md) | Ignore les n premiers éléments d'un tableau (complément de limit) |
| [`sort`](sort.md) | Trie un tableau : sur les éléments, ou sur une clef calculée par élément, du plus petit au plus grand (descending à true, ou un sens par clef, pour l'inverse) |
| [`stddev`](stddev.md) | Écart-type des nombres d'un tableau : de population par défaut, d'échantillon si sample vaut true |
| [`sum`](sum.md) | Somme des nombres d'un tableau (0 pour un tableau vide ou null) |
| [`sumby`](sumby.md) | Somme par clef calculée, en un objet { clef: somme } (la valeur par défaut est l'élément) |
| [`union`](union.md) | Aplatit d'un niveau un tableau de tableaux |
| [`unzip`](unzip.md) | Inverse de zip : d'un tableau de rangées, rend un tableau par position |
| [`variance`](variance.md) | Variance des nombres d'un tableau : de population par défaut, d'échantillon si sample vaut true |
| [`window`](window.md) | Fenêtres glissantes de size éléments consécutifs (vide si le tableau est plus court) |
| [`zip`](zip.md) | Apparie deux tableaux élément par élément, en s'arrêtant au plus court |

## [Encodage, empreintes et échappement](../encodage.md)

| Fonction | Description |
|---|---|
| [`crc32`](crc32.md) | Somme de contrôle CRC32 d'une valeur (entier non signé) |
| [`frombase64`](frombase64.md) | Décode un texte Base64 en texte UTF-8 |
| [`hexdecode`](hexdecode.md) | Relit un texte hexadécimal en chaîne UTF-8 |
| [`hexencode`](hexencode.md) | Écrit les octets UTF-8 d'une valeur en hexadécimal |
| [`hmacsha256`](hmacsha256.md) | Signature HMAC-SHA256 d'une valeur avec une clé secrète, en hexadécimal |
| [`htmlescape`](htmlescape.md) | Échappe les caractères qui ont un sens en HTML (< > & " ') |
| [`htmlunescape`](htmlunescape.md) | Remplace les entités HTML (&amp;, &lt;…) par leurs caractères |
| [`md5`](md5.md) | Empreinte MD5 d'une valeur, en hexadécimal (identité, pas signature) |
| [`sha1`](sha1.md) | Empreinte SHA-1 d'une valeur, en hexadécimal (identité, pas signature) |
| [`sha256`](sha256.md) | Empreinte SHA-256 d'une valeur, en hexadécimal |
| [`sha512`](sha512.md) | Empreinte SHA-512 d'une valeur, en hexadécimal |
| [`tobase64`](tobase64.md) | Encode une valeur en Base64 (texte UTF-8 ; objet ou tableau sérialisé en JSON) |
| [`urldecode`](urldecode.md) | Décode une valeur venue d'une URL (%20, %C3%A9…) |
| [`urlencode`](urlencode.md) | Encode une valeur pour une URL (mode path pour conserver les barres obliques) |

## [Expressions et opérateurs](../expressions.md)

| Fonction | Description |
|---|---|
| [`param`](param.md) | Valeur d'un paramètre externe passé à transform, ou la valeur de repli |
| [`params`](params.md) | Tous les paramètres externes de l'exécution, sous forme d'objet |
| [`uuid`](uuid.md) | Nouvel identifiant unique aléatoire (UUID v4) à chaque appel |

## [Nombres et maths](../nombres.md)

| Fonction | Description |
|---|---|
| [`abs`](abs.md) | Valeur absolue d'un nombre (null si ce n'est pas un nombre) |
| [`acos`](acos.md) | Arc cosinus, en radians |
| [`acosh`](acosh.md) | Arc cosinus hyperbolique |
| [`asin`](asin.md) | Arc sinus, en radians |
| [`asinh`](asinh.md) | Arc sinus hyperbolique |
| [`atan`](atan.md) | Arc tangente, en radians |
| [`atan2`](atan2.md) | Angle en radians du point (x = right, y = left) : atan2(y, x) |
| [`atanh`](atanh.md) | Arc tangente hyperbolique |
| [`ceil`](ceil.md) | Arrondi vers le haut, à l'entier (2.1 -> 3.0) ou à digits décimales |
| [`clamp`](clamp.md) | Ramène un nombre dans l'intervalle [lower, upper] |
| [`cos`](cos.md) | Cosinus d'un angle en radians |
| [`cosh`](cosh.md) | Cosinus hyperbolique |
| [`e`](e.md) | Constante e, base du logarithme népérien (2.71828…) |
| [`exp`](exp.md) | Exponentielle : e élevé à la puissance du nombre |
| [`floor`](floor.md) | Arrondi vers le bas, à l'entier (2.7 -> 2.0) ou à digits décimales |
| [`frombase`](frombase.md) | Lit un entier écrit dans une base de 2 à 36 |
| [`fromhex`](fromhex.md) | Lit un entier écrit en hexadécimal (avec ou sans préfixe 0x) |
| [`gcd`](gcd.md) | Plus grand commun diviseur de deux entiers |
| [`isfinite`](isfinite.md) | Vrai si la valeur est un nombre fini (ni infini, ni NaN) |
| [`isnan`](isnan.md) | Vrai si la valeur est le résultat indéfini d'un calcul (NaN) |
| [`log`](log.md) | Logarithme d'un nombre dans la base donnée |
| [`logarithm`](logarithm.md) | Logarithme népérien (base e) d'un nombre |
| [`logarithm10`](logarithm10.md) | Logarithme décimal (base 10) d'un nombre |
| [`logarithm2`](logarithm2.md) | Logarithme binaire (base 2) d'un nombre |
| [`max`](max.md) | Plus grand de deux nombres, ou du tableau donné (décimal pour deux nombres) |
| [`min`](min.md) | Plus petit de deux nombres, ou du tableau donné (décimal pour deux nombres) |
| [`parsenumber`](parsenumber.md) | Lit un nombre écrit en texte selon une culture (1 234,56 en fr-FR) |
| [`pi`](pi.md) | Constante pi (3.14159…) |
| [`pow`](pow.md) | Puissance : base élevée à l'exposant, rendue en décimal |
| [`round`](round.md) | Arrondi à l'entier le plus proche, demi vers le pair (2.5 -> 2.0, 3.5 -> 4.0), rendu en décimal |
| [`shiftleft`](shiftleft.md) | Décale les bits d'un entier vers la gauche (multiplie par 2^bits) |
| [`shiftright`](shiftright.md) | Décale les bits d'un entier vers la droite (divise par 2^bits) |
| [`sign`](sign.md) | Signe d'un nombre : -1, 0 ou 1 |
| [`sin`](sin.md) | Sinus d'un angle en radians |
| [`sinh`](sinh.md) | Sinus hyperbolique |
| [`sqrt`](sqrt.md) | Racine carrée d'un nombre |
| [`tan`](tan.md) | Tangente d'un angle en radians |
| [`tanh`](tanh.md) | Tangente hyperbolique |
| [`tobase`](tobase.md) | Écrit un entier dans une base de 2 à 36, complété à width chiffres |
| [`tohex`](tohex.md) | Écrit un entier en hexadécimal minuscule, complété à width chiffres |
| [`truncate`](truncate.md) | Coupe vers zéro (-2.7 -> -2.0), à l'entier ou à digits décimales |

## [Objets et structures profondes](../objets.md)

| Fonction | Description |
|---|---|
| [`entries`](entries.md) | Paires d'un objet en tableau de { key, value }, dans l'ordre du document |
| [`flattenobject`](flattenobject.md) | Aplatit un objet en clés pointées (a.b.c), tableaux indexés par leur position |
| [`fromentries`](fromentries.md) | Reconstruit un objet depuis un tableau de { key, value } ou de paires [clé, valeur] |
| [`has`](has.md) | Vrai si l'objet porte cette clé, même avec une valeur nulle |
| [`keys`](keys.md) | Clés d'un objet, dans l'ordre du document (null si ce n'est pas un objet) |
| [`merge`](merge.md) | Fusionne deux objets, la droite gagnant les clés communes (deep pour les sous-objets, arrays pour concaténer les tableaux) |
| [`omit`](omit.md) | Objet privé des clés demandées (une clé ou un tableau de clés) |
| [`pick`](pick.md) | Sous-objet limité aux clés demandées (une clé ou un tableau de clés) |
| [`prune`](prune.md) | Retire récursivement les null d'une structure, et le vide avec l'option empty |
| [`renamekeys`](renamekeys.md) | Renomme les clés d'un objet selon un mapping { ancien: nouveau } |
| [`setpath`](setpath.md) | Copie de l'objet avec une valeur posée au bout d'un chemin pointé (niveaux créés au besoin) |
| [`unflatten`](unflatten.md) | Reconstruit un objet imbriqué depuis des clés pointées (arrays à true pour les indices) |
| [`unsetpath`](unsetpath.md) | Copie de l'objet privée du chemin pointé (sans erreur s'il est absent) |
| [`values`](values.md) | Valeurs d'un objet, dans l'ordre du document (null si ce n'est pas un objet) |
| [`walk`](walk.md) | Applique une expression à chaque nœud d'une structure, des feuilles vers la racine |

## [Qualité : refuser, observer, valider](../qualite.md)

| Fonction | Description |
|---|---|
| [`isemail`](isemail.md) | Vrai si le texte a la forme d'une adresse électronique |
| [`isiban`](isiban.md) | Vrai si le texte est un IBAN dont la clé de contrôle (modulo 97) est juste |
| [`isurl`](isurl.md) | Vrai si le texte a la forme d'une URL avec son schéma |
| [`isuuid`](isuuid.md) | Vrai si le texte a la forme d'un UUID (accolades tolérées) |
| [`require`](require.md) | Rend la valeur si elle est présente, sinon lève avec le message donné |
| [`requirethat`](requirethat.md) | Vérifie une condition et lève avec le message donné si elle n'est pas vraie |
| [`trace`](trace.md) | Rend la valeur inchangée et l'enregistre dans le journal, lisible par traces() |
| [`traces`](traces.md) | Journal des valeurs observées par trace() dans cette exécution |

## [Sortie texte](../sortie.md)

| Fonction | Description |
|---|---|
| [`to_block`](to_block.md) | Sortie : une ligne JSON compacte par élément du tableau résultat (JSON Lines), ou l'objet résultat sur une ligne |
| [`to_csv`](to_csv.md) | Sortie : le tableau résultat en CSV (séparateur et ligne d'en-tête réglables) |
| [`to_json`](to_json.md) | Sortie : sérialise le résultat en JSON, indenté si indented vaut true ; ignore_null_and_empty_value retire les propriétés nulles ou vides |
| [`to_xml`](to_xml.md) | Sortie : le résultat en XML sous l'élément racine donné (@clef = attribut, #text = contenu) |
| [`to_yaml`](to_yaml.md) | Sortie : le résultat en YAML, en style bloc ou en style JSON si json_style vaut true |

## [Texte, expressions régulières et formatage](../texte.md)

| Fonction | Description |
|---|---|
| [`deaccent`](deaccent.md) | Retire les diacritiques (accents, cédilles) sans toucher à la casse |
| [`endswith`](endswith.md) | Vrai si le texte se termine par txt |
| [`foldtext`](foldtext.md) | Clef de comparaison d'un texte : minuscules sans accents par défaut, ou seulement case / accents |
| [`format`](format.md) | Formate un nombre ou une date ISO selon un masque (N2, #,##0.00, dd/MM/yyyy…) et une culture |
| [`indexof`](indexof.md) | Position (à partir de 0) de la première occurrence dans un texte ou un tableau, -1 si absent |
| [`lastindexof`](lastindexof.md) | Position (à partir de 0) de la dernière occurrence dans un texte ou un tableau, -1 si absent |
| [`levenshtein`](levenshtein.md) | Nombre de caractères à insérer, supprimer ou remplacer pour passer d'un texte à l'autre |
| [`lower`](lower.md) | Texte en minuscules (null reste null, une non-chaîne donne false) |
| [`normalize`](normalize.md) | Normalise une chaîne Unicode : forme C (défaut), D, KC ou KD |
| [`padleft`](padleft.md) | Complète le texte à gauche jusqu'à length avec le 1er caractère de charset (espace par défaut) |
| [`padright`](padright.md) | Complète le texte à droite jusqu'à length avec le 1er caractère de charset (espace par défaut) |
| [`regexismatch`](regexismatch.md) | Vrai si le texte contient une correspondance du motif regex |
| [`regexmatches`](regexmatches.md) | Liste des correspondances du motif regex dans le texte |
| [`regexreplace`](regexreplace.md) | Remplace les correspondances d'un motif regex ($1, ${nom}, $& pour les groupes) |
| [`repeat`](repeat.md) | Répète le texte count fois (0 ou négatif : chaîne vide) |
| [`replace`](replace.md) | Remplace toutes les occurrences de search par replacement |
| [`shorten`](shorten.md) | Raccourcit un texte à length caractères au plus, suffixe compris (… par défaut) |
| [`similarity`](similarity.md) | Proximité de deux textes entre 0 (tout diffère) et 1 (identiques) |
| [`slugify`](slugify.md) | Transforme un texte en identifiant d'URL : sans accent, en minuscules, mots joints par un tiret |
| [`split`](split.md) | Découpe un texte en tableau sur le premier caractère de charset |
| [`splitregex`](splitregex.md) | Découpe un texte sur les correspondances d'un motif regex |
| [`splitstring`](splitstring.md) | Découpe un texte sur un séparateur complet (plusieurs caractères), au plus limit fois |
| [`startswith`](startswith.md) | Vrai si le texte commence par txt |
| [`stringcontains`](stringcontains.md) | Vrai si le texte contient contain_str |
| [`stringlenght`](stringlenght.md) | Nombre de caractères d'un texte (0 pour null ou une non-chaîne) — orthographe d'origine conservée |
| [`substring`](substring.md) | Extrait length caractères à partir de start (start négatif = depuis la fin, length absente = jusqu'au bout) |
| [`titlecase`](titlecase.md) | Met en majuscule la première lettre de chaque mot, sans toucher au reste |
| [`trim`](trim.md) | Retire les espaces en début et fin, ou les caractères de txt s'il est donné |
| [`trimend`](trimend.md) | Retire les espaces en fin, ou les caractères de txt |
| [`trimstart`](trimstart.md) | Retire les espaces en début, ou les caractères de txt |
| [`upper`](upper.md) | Texte en majuscules (null reste null, une non-chaîne donne false) |

## [Types, repli sur erreur et validation](../types.md)

| Fonction | Description |
|---|---|
| [`isarray`](isarray.md) | Vrai si la valeur est un tableau JSON |
| [`isboolean`](isboolean.md) | Vrai si la valeur est un booléen (true ou false) |
| [`isnotnull`](isnotnull.md) | Vrai si la valeur n'est ni null ni absente |
| [`isnull`](isnull.md) | Vrai si la valeur est null ou absente |
| [`isnumber`](isnumber.md) | Vrai si la valeur est un nombre (un booléen n'en est pas un) |
| [`isobject`](isobject.md) | Vrai si la valeur est un objet JSON |
| [`isstring`](isstring.md) | Vrai si la valeur est une chaîne de caractères |
| [`parsejson`](parsejson.md) | Lit un texte JSON et rend la valeur correspondante (objet, tableau ou scalaire) |
| [`schema`](schema.md) | JSON Schema (draft-04) déduit d'un fragment JSON d'exemple |
| [`schemaerrors`](schemaerrors.md) | Liste des erreurs de validation d'un document contre un JSON Schema (vide si conforme) |
| [`schemaisvalid`](schemaisvalid.md) | Vrai si le document respecte le JSON Schema donné (sous-ensemble géré) |
| [`trydefault`](trydefault.md) | Valeur de l'expression, ou celle du repli si l'expression lève une erreur |
| [`typeof`](typeof.md) | Type JSON d'une valeur : null, boolean, number, string, array ou object |

---

[← Guide jslt](../guide.md)
