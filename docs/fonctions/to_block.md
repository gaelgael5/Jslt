<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `to_block`

*Français · [English](to_block.en.md)*

Sortie : une ligne JSON compacte par élément du tableau résultat (JSON Lines), ou l'objet résultat sur une ligne

```
to_block()
```

**Exemple**

```jslt
{ "$directives": { "output": { "filter": $.lignes, "mode": to_block() } }, "lignes": $.l[*] }
```

```json
{ "l": [{ "id": 1 }, { "id": 2 }] }
```

```json
{ "lignes": [{ "id": 1 }, { "id": 2 }] }
```

`render()` produit :

```text
{"id":1}
{"id":2}
```

Cette fonction ne prend aucun argument.

Fonction de **sortie** : elle ne s'appelle pas dans le corps du template, mais se déclare dans `"$directives": {"output": {"mode": …}}`.

**Chapitre** : [Sortie texte](../sortie.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
