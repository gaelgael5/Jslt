<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `to_yaml`

*Français · [English](to_yaml.en.md)*

Sortie : le résultat en YAML, en style bloc ou en style JSON si json_style vaut true

```
to_yaml(json_style)
```

**Exemple**

```jslt
{ "$directives": { "output": { "filter": $.client, "mode": to_yaml() } }, "client": { "id": $.id, "ville": $.v } }
```

```json
{ "id": 1, "v": "Lyon" }
```

```json
{ "client": { "id": 1, "ville": "Lyon" } }
```

`render()` produit :

```text
id: 1
ville: Lyon
```

| Paramètre | Attendu | Note |
|---|---|---|
| `json_style` | optionnel |  |

Fonction de **sortie** : elle ne s'appelle pas dans le corps du template, mais se déclare dans `"$directives": {"output": {"mode": …}}`.

**À savoir**

- Sous-ensemble assumé : ni ancres, ni tags, ni littéral multi-ligne. Tout scalaire relisible comme un autre type est **cité** — un texte `"true"` ou `"12"` reste un texte.

**Chapitre** : [Sortie texte](../sortie.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
