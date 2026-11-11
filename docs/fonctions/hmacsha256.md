<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `hmacsha256`

*Français · [English](hmacsha256.en.md)*

Signature HMAC-SHA256 d'une valeur avec une clé secrète, en hexadécimal

```
hmacsha256(token, key)
```

**Exemple**

```jslt
{ "r": hmacsha256($.t, $.cle) }
```

```json
{ "t": "message", "cle": "secret" }
```

```json
{ "r": "8b5f48702995c1598c573db1e21866a9b825d4a794d169d7060a03605796360b" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `key` | optionnel |  |

**Chapitre** : [Encodage, empreintes et échappement](../encodage.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
