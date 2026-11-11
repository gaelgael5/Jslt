<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `isiban`

*Français · [English](isiban.en.md)*

Vrai si le texte est un IBAN dont la clé de contrôle (modulo 97) est juste

```
isiban(token)
```

**Exemple**

```jslt
{ "r": isiban($.t) }
```

```json
{ "t": "FR7630006000011234567890189" }
```

```json
{ "r": true }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**À savoir**

- Vérifie la structure et la **clé modulo 97**, mais pas la longueur par pays : ce serait une table de soixante entrées dont la péremption ferait refuser un IBAN valide.

**Chapitre** : [Qualité : refuser, observer, valider](../qualite.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
