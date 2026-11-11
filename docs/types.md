# Types, repli sur erreur et validation — guide jslt

*Français · [English](types.en.md)*

[← Guide jslt](guide.md) · les exemples de cette page sont **exécutés par la
suite de tests** (`tests/test_guide_examples.py`), sous la forme de triplets
*template → entrée → sortie*.

---

## Interroger le type : `typeof` et les prédicats

Le moteur ne savait dire que `isnull` / `isnotnull`. Un champ tantôt scalaire,
tantôt liste — cas banal d'un export hérité — n'était donc pas traitable.

`typeof(valeur)` rend le nom du type JSON : `null`, `boolean`, `number`,
`string`, `array` ou `object` ; c'est le vocabulaire de JSON Schema, pour que le
même mot serve ici et dans un schéma. Les prédicats `isarray`, `isobject`,
`isstring`, `isnumber` et `isboolean` rendent un booléen, et **faux** sur `null`.

Un booléen n'est **pas** un nombre : `isnumber(true)` est faux, comme en JSON.

```jslt
{
  "forme": typeof($.valeur),
  "liste": when(isarray($.valeur)) { "true": $.valeur, "default": [$.valeur] }
}
```

```json
{ "valeur": "seule" }
```

```json
{ "forme": "string", "liste": ["seule"] }
```

## Repli sur erreur : `trydefault`

`??` traite la valeur **absente**. `trydefault(expression, repli)` traite
l'expression qui **échoue** : division par zéro, cast impossible, fonction qui
refuse ses données. Les deux arguments sont évalués paresseusement — le repli ne
l'est que s'il sert, donc il peut être coûteux sans pénaliser le cas normal.

Seules les erreurs du moteur (`JsltError`) sont rattrapées. Une construction
**non portée** (`NotImplementedError`) passe au travers : c'est un trou du
moteur, pas une donnée fautive, et la rattraper le ferait passer pour un cas
limite.

```jslt
{
  "taux": trydefault($.part / $.total, 0),
  "quantite": trydefault($.qte #integer, -1)
}
```

```json
{ "part": 3, "total": 0, "qte": "douze" }
```

```json
{ "taux": 0, "quantite": -1 }
```

## Lire du JSON encodé dans une chaîne : `parsejson`

`to_json` est une fonction de **sortie**, refusée dans le corps du template : il
n'existait aucun chemin de retour. `parsejson(texte)` ouvre une chaîne qui
*contient* du JSON — colonne texte d'une base, charge utile encapsulée, réponse
stockée. Un texte invalide **lève** plutôt que de rendre `null` : une charge
utile corrompue qui produirait un résultat vide se découvrirait très loin de sa
cause. Avec `trydefault`, le repli reste à votre main.

```jslt
{ "ville": parsejson($.payload) -> select($.adresse.ville) }
```

```json
{ "payload": "{\"adresse\":{\"ville\":\"Lyon\"}}" }
```

```json
{ "ville": "Lyon" }
```

---

## Valider contre un schéma : `schemaerrors`, `schemaisvalid`

`schema` **déduit** un schéma d'un exemple ; ces deux fonctions font l'inverse,
elles **confrontent** un document à un schéma. `schemaerrors` rend la liste des
erreurs, chacune localisée (`$.tags[1] : attendu une chaîne, reçu un nombre`) ;
`schemaisvalid` rend un booléen. Rendre la liste plutôt qu'un simple booléen est
ce qui permet de refuser un flux **en expliquant pourquoi**.

Mots-clés vérifiés : `$ref` (interne, vers `definitions`), `type` (dont
`integer`), `enum`, `properties`, `additionalProperties: false`, `required`,
`items` (schéma unique ou par position), `minItems`, `maxItems`, `uniqueItems`,
`minimum`, `maximum`, `exclusiveMinimum`, `exclusiveMaximum` (formes draft-04
booléenne et draft-06 numérique), `minLength`, `maxLength`, `pattern`, et les
`format` que `schema` produit (`date`, `date-time`, `duration`).

**Les mots-clés inconnus sont ignorés**, volontairement : `allOf`, `oneOf`, un
`$ref` externe… ne font pas refuser le schéma, ils ne sont simplement pas
vérifiés. Lever rendrait la fonction inutilisable sur les schémas réels ; le prix
est qu'un document peut être déclaré valide alors qu'un mot-clé non géré l'aurait
rejeté. C'est une validation **utile**, pas une validation **complète**.

```jslt
{
  "conforme": schemaisvalid($.client, $.modele),
  "erreurs": schemaerrors($.client, $.modele)
}
```

```json
{
  "modele": {
    "type": "object",
    "required": ["nom", "age"],
    "properties": { "nom": { "type": "string" }, "age": { "type": "integer", "minimum": 0 } }
  },
  "client": { "nom": "Ana", "age": -1 }
}
```

```json
{
  "conforme": false,
  "erreurs": ["$.age : minimum 0 non respecté (reçu -1)"]
}
```

La boucle se ferme : ce que `schema` déduit valide l'exemple dont il est tiré.

---

## Schéma : `schema`

`schema(exemple)` déduit un JSON Schema (draft-04) d'un fragment JSON, comme
NJsonSchema côté .NET : objets imbriqués en `definitions` référencées.

```jslt
{ "s": schema($.exemple) }
```
```json
{ "exemple": { "nom": "Ana", "age": 30 } }
```
```json
{ "s": { "$schema": "http://json-schema.org/draft-04/schema#", "type": "object", "properties": { "nom": { "type": "string" }, "age": { "type": "integer" } } } }
```

---

**Voir aussi** : [Objets](objets.md) pour remodeler un objet dont on connaît
maintenant la forme, [Casts `#type`](expressions.md#casts-type) pour convertir.

---

[← Guide jslt](guide.md)
