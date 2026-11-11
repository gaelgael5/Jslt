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

**Voir aussi** : [Types et validation](types.md) pour savoir *si* une valeur est
un objet, [Données et collections](collections.md) pour les tableaux.

---

[← Guide jslt](guide.md)
