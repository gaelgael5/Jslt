<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `join`

*Français · [English](join.en.md)*

Jointure gauche : rattache aux objets de gauche les éléments de droite de même clé

```
join(source_left, key_left, clean_source, rights)
```

**Exemple**

```jslt
{ "r": join($.c, $.id, false, [{ "Name": "commandes", "Key": "$.client", "Source": $.o }]) }
```

```json
{ "c": [{ "id": 1, "nom": "Ana" }], "o": [{ "client": 1, "total": 12 }] }
```

```json
{ "r": [{ "id": 1, "nom": "Ana", "commandes": [{ "total": 12 }] }] }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `source_left` | optionnel |  |
| `key_left` | optionnel | chemin JSONPath **non évalué** |
| `clean_source` | optionnel |  |
| `rights` | optionnel |  |

**Chapitre** : [Données et collections](../collections.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
