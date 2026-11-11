<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `crc32`

*Français · [English](crc32.en.md)*

Somme de contrôle CRC32 d'une valeur (entier non signé)

```
crc32(token)
```

**Exemple**

```jslt
{ "r": crc32($.t) }
```

```json
{ "t": "abc" }
```

```json
{ "r": 891568578 }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |

**Chapitre** : [Encodage, empreintes et échappement](../encodage.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
