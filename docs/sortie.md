# Sortie texte — guide jslt

*Français · [English](sortie.en.md)*

[← Guide jslt](guide.md) · les exemples de cette page sont **exécutés par la
suite de tests** (`tests/test_guide_examples.py`), sous la forme de triplets
*template → entrée → sortie*.

---

Comme en .NET, un template peut déclarer comment son résultat est **sérialisé en
texte**. La clé `$directives` n'apparaît jamais dans le résultat de
`transform()` ; c'est `template.render(source)` qui l'applique : `filter`
(JSONPath, optionnel) sélectionne une partie du résultat (1 nœud → ce nœud,
plusieurs → tableau, aucun → `null`), puis la fonction de sortie `mode`
produit le texte.

```jslt
{ "$directives": { "output": { "filter": $.lignes, "mode": to_block() } },
  "lignes": $.commandes[*] }
```
```json
{ "commandes": [ { "id": 1 }, { "id": 2 } ] }
```
```json
{ "lignes": [ { "id": 1 }, { "id": 2 } ] }
```

`render()` donne ici une ligne JSON par élément (JSON Lines) :

```text
{"id":1}
{"id":2}
```

- `to_json(indented, ignore_null_and_empty_value)` : JSON compact, ou indenté si
  `indented` vaut `true` ; avec le 2e argument, les chaînes vides deviennent `null`
  et les propriétés nulles sont retirées des objets.
- `to_block()` : une ligne compacte par élément d'un tableau, ou l'objet sur une ligne.
- Sans directive, `render()` rend le JSON indenté du résultat.
- Les fonctions de sortie ne s'appellent pas dans le corps du template (erreur
  explicite) ; `mode` est obligatoire. Les fonctions d'écriture .NET (`write`,
  `to_file`) et `to_sqlserver` ne sont pas portées.

---

## Écrire autre chose que du JSON : `to_csv`, `to_xml`, `to_yaml`

Le moteur sait lire JSON, XML et CSV depuis une chaîne (`parsejson`,
[`parsexml`](https://github.com/gaelgael5/Jslt/tree/main/packages/urban-json-xml),
`parsecsv`) ; il écrit maintenant les trois. Les trois émetteurs sont **sans
dépendance** — une dépendance de plus dans le cœur se paie à chaque
installation — et suivent les conventions des lectures, pour que l'aller-retour
tienne.

| Fonction | Rôle |
|---|---|
| `to_csv(séparateur, entête)` | tableau d'objets → CSV (RFC 4180), `;` et en-tête par défaut |
| `to_xml(racine)` | document → XML sous cet élément racine |
| `to_yaml(style_json)` | document → YAML en style bloc, ou en style JSON |

**CSV.** Les colonnes sont l'**union des clés** rencontrées, dans l'ordre
d'apparition : se limiter à celles du premier objet perdrait des données sur un
flux hétérogène. Une cellule absente reste vide, ce qui est la façon dont un CSV
dit « rien ». Les valeurs imbriquées sont aplaties en clés pointées — la même
règle que [`flattenobject`](objets.md#structures-profondes), puisqu'un CSV n'a
pas de profondeur. Les guillemets sont doublés et les lignes finissent en CRLF,
comme l'exige la RFC.

**XML.** Conventions de `parsexml` : une clé préfixée `@` devient un
**attribut**, `#text` le contenu textuel, et une clé dont la valeur est un
tableau **répète** l'élément — c'est ainsi que XML exprime une liste. Un `null`
donne une balise vide plutôt que le texte « null ». Un nom d'élément invalide
lève, parce qu'un XML mal nommé n'est pas réparable en aval.

**YAML.** Style bloc, et un sous-ensemble assumé : pas d'ancres, pas de tags,
pas de style littéral multi-ligne. Ce qu'un lecteur relirait comme un autre type
est **cité** : un texte `"true"`, `"12"` ou `"null"` reste un texte. Avec
`to_yaml(true)`, la sortie est du JSON indenté — qui est du YAML valide, YAML 1.2
étant un sur-ensemble de JSON.

```jslt
{ "$directives": { "output": { "filter": $.lignes, "mode": to_csv() } },
  "lignes": [ { "$source": $.clients, "id": $.id, "ville": $.adr.ville } ] }
```

```json
{ "clients": [ { "id": 1, "adr": { "ville": "Lyon" } } ] }
```

```json
{ "lignes": [ { "id": 1, "ville": "Lyon" } ] }
```

`render()` donne ici :

```text
id;ville
1;Lyon
```

Reste non porté : l'écriture dans un fichier (`write` / `to_file`) et
`to_sqlserver`, par décision — une transformation rend du texte, c'est à
l'appelant de décider où il va.

---

[← Guide jslt](guide.md)
