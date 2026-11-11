<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `to_csv`

*Français · [English](to_csv.en.md)*

Sortie : le tableau résultat en CSV (séparateur et ligne d'en-tête réglables)

```
to_csv(separator, header)
```

**Exemple**

```jslt
{ "$directives": { "output": { "filter": $.lignes, "mode": to_csv() } }, "lignes": [ { "$source": $.clients, "id": $.id, "ville": $.adr.ville } ] }
```

```json
{ "clients": [{ "id": 1, "adr": { "ville": "Lyon" } }] }
```

```json
{ "lignes": [{ "id": 1, "ville": "Lyon" }] }
```

`render()` produit :

```text
id;ville
1;Lyon
```

| Paramètre | Attendu | Note |
|---|---|---|
| `separator` | optionnel |  |
| `header` | optionnel |  |

Fonction de **sortie** : elle ne s'appelle pas dans le corps du template, mais se déclare dans `"$directives": {"output": {"mode": …}}`.

**Chapitre** : [Sortie texte](../sortie.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
