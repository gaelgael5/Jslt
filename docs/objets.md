# Objets : clés, valeurs et remodelage — guide jslt

*Français · [English](objets.en.md)*

[← Guide jslt](guide.md) · les exemples de cette page sont **exécutés par la
suite de tests** (`tests/test_guide_examples.py`), sous la forme de triplets
*template → entrée → sortie*.

---

Un template construit ses objets **clé par clé**, littéralement. Dès que les
clés ne sont connues qu'à l'exécution — un dictionnaire de tarifs, des colonnes
variables, un objet à filtrer — il faut les manipuler comme des données : c'est
ce que font ces fonctions.

| Fonction | Rôle |
|---|---|
| `keys(objet)` | ses clés, dans l'ordre du document |
| `values(objet)` | ses valeurs, dans le même ordre |
| `entries(objet)` | `[{ "key": …, "value": … }]` |
| `fromentries(tableau)` | l'inverse : reconstruit l'objet |
| `merge(a, b, profond)` | fusionne, la **droite gagne** les clés communes |
| `pick(objet, clés)` | sous-objet limité aux clés demandées |
| `omit(objet, clés)` | objet privé de ces clés |
| `has(objet, clé)` | la clé est **présente**, même valant `null` |
| `renamekeys(objet, mapping)` | renomme selon `{ ancien: nouveau }` |

**Conventions.** `null` et une valeur qui n'est pas un objet donnent `null` — un
tableau n'est pas « un objet sans clés », et rendre `{}` laisserait croire à un
objet vide. `pick` et `omit` acceptent une clé seule (`pick($.o, "a")`) ou un
tableau ; une clé demandée mais absente est simplement absente du résultat, sans
erreur, parce que c'est exactement sur des documents hétérogènes qu'on s'en sert.
Aucune fonction ne modifie son entrée.

**`has` contre `isnull`.** `isnull($.o.a)` est vrai pour une clé absente *comme*
pour une clé présente valant `null`. Quand la distinction compte — champ non
renseigné contre champ absent du flux — c'est `has` qu'il faut.

```jslt
{
  "clefs": keys($.client),
  "sans_interne": omit($.client, ["interne", "trace"]),
  "a_un_mail": has($.client, "mail"),
  "mail_vide": isnull($.client.mail)
}
```

```json
{ "client": { "nom": "Ana", "mail": null, "interne": true, "trace": "x" } }
```

```json
{
  "clefs": ["nom", "mail", "interne", "trace"],
  "sans_interne": { "nom": "Ana", "mail": null },
  "a_un_mail": true,
  "mail_vide": true
}
```

**Fusion.** `merge` est **plate** par défaut : une clé commune est remplacée, y
compris si sa valeur est un objet. Le troisième argument à `true` descend dans
les sous-objets.

```jslt
{
  "plat": merge($.defauts, $.client),
  "profond": merge($.defauts, $.client, true)
}
```

```json
{
  "defauts": { "options": { "langue": "fr", "theme": "clair" } },
  "client": { "options": { "theme": "sombre" } }
}
```

```json
{
  "plat": { "options": { "theme": "sombre" } },
  "profond": { "options": { "langue": "fr", "theme": "sombre" } }
}
```

**Parcourir un objet.** `entries` rend des objets nommés — `$.key` et `$.value`
se lisent dans une boucle, là où des paires `[clé, valeur]` imposeraient un accès
par indice, muet à la relecture. Avec `fromentries`, l'aller-retour permet de
transformer les clés elles-mêmes.

```jslt
{
  "inverse": fromentries([
    { "$source": entries($.tarifs), "key": $.value #string, "value": $.key }
  ])
}
```

```json
{ "tarifs": { "petit": 10, "grand": 20 } }
```

```json
{ "inverse": { "10": "petit", "20": "grand" } }
```

**Renommer.** `renamekeys` laisse intactes les clés absentes du mapping. En cas
de collision (renommer `a` en `b` alors que `b` existe), le **dernier écrit
gagne**, dans l'ordre du document : lever serait plus strict, mais rendrait le
renommage impraticable sur un flux qui porte les deux noms pendant une migration.

```jslt
{ "normalise": renamekeys($.ligne, { "lib": "libelle", "qte": "quantite" }) }
```

```json
{ "ligne": { "lib": "Vis", "qte": 12, "prix": 3 } }
```

```json
{ "normalise": { "libelle": "Vis", "quantite": 12, "prix": 3 } }
```

---

## Accès par clef calculée : `get`, `getpath`

Un chemin est **littéral** : `$.tarifs.petit` s'écrit dans le template. Quand la
clef vient des **données**, `$.tarifs[$.formule]` n'est pas un chemin pris en
charge, et il fallait ce détour — quatre fonctions et une variable pour un accès
par clef.

| Fonction | Rôle |
|---|---|
| `get(v, clef)` | une clef d'objet **ou** un indice de tableau, tous deux calculés ; `-1` = dernier |
| `getpath(v, chemin, séparateur)` | un chemin pointé calculé (`"client.ville"`), réciproque de `setpath` |

```jslt
{ "f:": $.formule, "detour": first(map(filter(entries($.tarifs), $.key == f:), $.value)), "direct": get($.tarifs, $.formule) }
```
```json
{ "tarifs": { "petit": 10, "grand": 20 }, "formule": "grand" }
```
```json
{ "detour": 20, "direct": 20 }
```

Clef absente, indice hors bornes, source qui n'est ni objet ni tableau : `null`,
la convention de la famille. Il n'y a donc **pas** d'argument de repli : `??` le
dit déjà, et un repli en argument serait évalué même quand la clef existe. Pour
*exiger* la valeur, [`require`](qualite.md#refuser--require-requirethat) refuse
et nomme la cause (`require(get($.tarifs, $.formule), "tarif inconnu")`). Pour
distinguer une clef absente d'une clef présente valant `null`, c'est `has`.

```jslt
{ "ville": getpath($.doc, $.champ), "dernier": get($.l, -1), "repli": get($.tarifs, "moyen") ?? 0 }
```
```json
{ "doc": { "client": { "ville": "Lyon" } }, "champ": "client.ville", "l": [1, 2, 3], "tarifs": { "petit": 10 } }
```
```json
{ "ville": "Lyon", "dernier": 3, "repli": 0 }
```

Les étapes de `getpath` se lisent comme celles de `setpath`, indices de tableau
compris (`"lignes.0.ref"`), et le séparateur se règle par le 3e argument.

---

## Structures profondes

Lire profond se faisait déjà (`$..k`) ; **transformer** profond manquait.

| Fonction | Rôle |
|---|---|
| `flattenobject(o, séparateur)` | objet imbriqué → clés pointées (`adr.ville`), tableaux indexés |
| `unflatten(o, séparateur, tableaux)` | l'inverse ; `tableaux` à `true` pour relire les indices |
| `walk(v, expression)` | applique une expression à **chaque nœud**, des feuilles vers la racine |
| `prune(v, options)` | retire récursivement les `null`, et le vide avec `"empty"` |
| `setpath(o, chemin, valeur)` | copie avec une valeur posée au bout d'un chemin |
| `unsetpath(o, chemin)` | copie privée de ce chemin |

**Aplatir.** C'est le pont vers un format tabulaire, et `to_csv` l'emprunte.
Un conteneur **vide** est conservé comme feuille (`{"a": {}}` reste
`{"a": {}}`), sans quoi l'aller-retour perdrait l'information.

**Reconstruire.** Les segments numériques ne redeviennent des tableaux que si on
le demande : une clé `2026` est un nom d'année dans bien des documents, et en
faire un indice créerait un tableau de deux mille trous. Un chemin qui en
contredit un autre (`a` valant 1 **et** `a.b` valant 2) **lève** : écraser
silencieusement ferait disparaître une donnée.

```jslt
{
  "plat": flattenobject($.client),
  "retour": unflatten(flattenobject($.client), ".", true)
}
```

```json
{ "client": { "id": 1, "adr": { "ville": "Lyon" }, "tags": ["a", "b"] } }
```

```json
{
  "plat": { "id": 1, "adr.ville": "Lyon", "tags.0": "a", "tags.1": "b" },
  "retour": { "id": 1, "adr": { "ville": "Lyon" }, "tags": ["a", "b"] }
}
```

**Parcourir.** `walk` remonte **des feuilles vers la racine** : l'expression voit
des enfants déjà transformés, donc une règle qui dépend d'eux fonctionne. Dans
l'autre sens, elle verrait l'original et devrait redescendre elle-même.

`prune` ne retire que les `null` par défaut : une chaîne vide, un tableau vide et
`0` sont des **valeurs**, et les supprimer d'office ferait disparaître un
« montant : 0 » qui dit quelque chose. L'option `"empty"` est là pour qui veut
l'inverse — elle garde `0` et `false`, qui ne sont pas vides.

```jslt
{
  "propre": prune($.doc),
  "rognes": walk($.doc, when(isstring($)) { "true": trim($), "default": $ })
}
```

```json
{ "doc": { "a": " x ", "b": null, "l": [" y ", null] } }
```

```json
{
  "propre": { "a": " x ", "l": [" y "] },
  "rognes": { "a": "x", "b": null, "l": ["y", null] }
}
```

**Poser et retirer.** `setpath` crée les niveaux manquants et traverse les
tableaux par indice (`l.1.v`) ; il **lève** s'il devait écraser un scalaire pour
descendre. `unsetpath` ne lève pas sur un chemin absent : on demande un document
sans cette donnée, et il l'est déjà. Ni l'un ni l'autre ne modifie sa source.

```jslt
{ "r": setpath($.o, "adr.pays", "FR") -> unsetpath("interne") }
```

```json
{ "o": { "adr": { "ville": "Lyon" }, "interne": true } }
```

```json
{ "r": { "adr": { "ville": "Lyon", "pays": "FR" } } }
```

Enfin, `merge` accepte un 4e argument : `merge(a, b, true, true)` **concatène**
les tableaux au lieu de les remplacer. Le remplacement reste le défaut, parce que
fusionner deux listes de longueurs différentes n'a pas de sens unique.

---

**Voir aussi** : [Types et validation](types.md) pour savoir *si* une valeur est
un objet, [Données et collections](collections.md) pour les tableaux.

---

[← Guide jslt](guide.md)
