<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `now`

*Français · [English](now.en.md)*

Date et heure courantes en ISO 8601 : locales, ou UTC si utc vaut true

```
now(utc)
```

**Exemple**

```jslt
{ "r": datepart(now(), "year") >= 2026 }
```

```json
{}
```

```json
{ "r": true }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `utc` | optionnel |  |

**À savoir**

- Non déterministe : deux appels dans le même template peuvent différer. Pour un template **testable**, passer l'instant en paramètre externe (`param("date_reference")`) plutôt que d'appeler `now()`.

**Chapitre** : [Dates et heures](../dates.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
