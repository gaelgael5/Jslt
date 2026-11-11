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

**À savoir**

- Les colonnes sont l'**union des clés** rencontrées, dans l'ordre d'apparition : s'arrêter au premier objet perdrait des données sur un flux hétérogène.
- Les valeurs imbriquées sont aplaties en clés pointées (`flattenobject`), les guillemets doublés et les lignes finies en CRLF, comme l'exige la RFC 4180.

**Chapitre** : [Sortie texte](../sortie.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
