<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `to_json`

*Français · [English](to_json.en.md)*

Sortie : sérialise le résultat en JSON, indenté si indented vaut true ; ignore_null_and_empty_value retire les propriétés nulles ou vides

```
to_json(indented, ignore_null_and_empty_value)
```

**Exemple**

```jslt
{ "$directives": { "output": { "mode": to_json(true) } }, "ville": $.v }
```

```json
{ "v": "Lyon" }
```

```json
{ "ville": "Lyon" }
```

`render()` produit :

```text
{
  "ville": "Lyon"
}
```

| Paramètre | Attendu | Note |
|---|---|---|
| `indented` | optionnel |  |
| `ignore_null_and_empty_value` | optionnel |  |

Fonction de **sortie** : elle ne s'appelle pas dans le corps du template, mais se déclare dans `"$directives": {"output": {"mode": …}}`.

**À savoir**

- `ignore_null_and_empty_value` transforme les chaînes vides en `null` **puis** retire les propriétés nulles des objets ; les tableaux gardent leurs éléments.

**Chapitre** : [Sortie texte](../sortie.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
