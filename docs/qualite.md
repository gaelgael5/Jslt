# Qualité : refuser, observer, valider — guide jslt

*Français · [English](qualite.en.md)*

[← Guide jslt](guide.md) · les exemples de cette page sont **exécutés par la
suite de tests** (`tests/test_guide_examples.py`), sous la forme de triplets
*template → entrée → sortie*.

---

Deux choses manquaient à un template pour être tenable en production : pouvoir
**refuser** une donnée, et pouvoir **regarder** ce qu'il fait.

## Refuser : `require`, `requirethat`

Sans elles, un template confronté à une donnée inacceptable n'avait que deux
issues : produire une sortie fausse, ou provoquer une erreur par accident (une
division par zéro bien placée). Le refus est maintenant explicite et porte un
**message métier**.

- `require(valeur, message)` rend la valeur si elle est **présente**, sinon lève.
  Seule l'absence (`null`) est refusée : `0`, `false`, `""` et `[]` sont des
  valeurs, et les refuser rendrait la fonction inutilisable sur un montant nul.
- `requirethat(condition, message)` exige une condition **vraie**, strictement.
  Une condition qui vaut `0` ou `""` est presque toujours une expression qu'on
  croyait booléenne : la laisser passer pour fausse masquerait l'erreur
  d'écriture.

Les deux lèvent une `JsltError`, donc dans la même famille que le reste du
moteur : `trydefault` peut les rattraper quand le refus doit rester local.

```jslt
{
  "id": require($.id, "identifiant client obligatoire"),
  "remise": trydefault(require($.remise, "absente"), 0)
}
```

```json
{ "id": "C-12" }
```

```json
{ "id": "C-12", "remise": 0 }
```

## Observer : `trace`, `traces`

Le pas-à-pas existe au niveau de l'API (`JsltTemplate.debug`), pas du langage :
impossible de regarder une valeur intermédiaire sans l'ajouter au résultat, donc
sans changer ce qu'on mesure.

`trace(valeur, étiquette)` rend la valeur **inchangée** et l'enregistre.
`traces()` rend le journal de l'exécution courante, que le template peut placer
où il veut — ou nulle part, un intégrateur le lisant alors sur le contexte
(`context.traces`, cf. [Intégrer le moteur](integration.md)).

Le journal vit sur le contexte d'exécution : deux exécutions, même concurrentes,
ne voient jamais les traces l'une de l'autre.

```jslt
{
  "total": trace($.a, "a") + trace($.b, "b"),
  "_diagnostic": traces()
}
```

```json
{ "a": 2, "b": 3 }
```

```json
{
  "total": 5,
  "_diagnostic": [ { "label": "a", "value": 2 }, { "label": "b", "value": 3 } ]
}
```

## Valider un format : `isemail`, `isurl`, `isuuid`, `isiban`

Quatre prédicats, volontairement **pragmatiques**. Une adresse conforme à la RFC
5322 complète accepte des formes que personne n'utilise (commentaires,
guillemets) : un validateur qui les accepte laisse passer ce qu'un système en
aval refusera.

`isiban` vérifie la structure **et** la clé de contrôle (modulo 97), qui attrape
les fautes de frappe. La longueur attendue par pays n'est pas vérifiée : ce
serait une table de plus de soixante entrées à maintenir, et sa péremption ferait
refuser un IBAN valide — un faux refus coûte plus cher ici qu'un faux accord, que
la banque rejettera de toute façon.

Ces prédicats rendent un **booléen** : `null` et un nombre ne sont pas des
adresses valides, et rendre `null` obligerait l'appelant à distinguer trois cas
là où la question est fermée.

```jslt
{
  "mail": requirethat(isemail($.mail), "adresse électronique invalide"),
  "iban_ok": isiban($.iban)
}
```

```json
{ "mail": "a.b@exemple.fr", "iban": "FR1420041010050500013M02606" }
```

```json
{ "mail": true, "iban_ok": true }
```

---

**Voir aussi** : [Types et validation](types.md) pour valider une **forme**
entière contre un JSON Schema, [Intégrer le moteur](integration.md) pour lire les
traces depuis le code appelant.

---

[← Guide jslt](guide.md)
