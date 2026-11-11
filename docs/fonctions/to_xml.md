<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `to_xml`

*Français · [English](to_xml.en.md)*

Sortie : le résultat en XML sous l'élément racine donné (@clef = attribut, #text = contenu)

```
to_xml(root)
```

**Exemple**

```jslt
{ "$directives": { "output": { "filter": $.client, "mode": to_xml("client") } }, "client": { "@id": $.id, "ville": $.v } }
```

```json
{ "id": 1, "v": "Lyon" }
```

```json
{ "client": { "@id": 1, "ville": "Lyon" } }
```

`render()` produit :

```text
<?xml version="1.0" encoding="utf-8"?>
<client id="1"><ville>Lyon</ville></client>
```

| Paramètre | Attendu | Note |
|---|---|---|
| `root` | optionnel |  |

Fonction de **sortie** : elle ne s'appelle pas dans le corps du template, mais se déclare dans `"$directives": {"output": {"mode": …}}`.

**À savoir**

- Conventions de `parsexml` : une clé préfixée `@` devient un **attribut**, `#text` le contenu textuel, et une clé dont la valeur est un tableau **répète** l'élément. Un nom d'élément invalide lève.

**Chapitre** : [Sortie texte](../sortie.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
