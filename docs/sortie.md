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

[← Guide jslt](guide.md)
