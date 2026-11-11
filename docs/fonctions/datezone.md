<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datezone`

*Français · [English](datezone.en.md)*

Attribue un fuseau à une date sans décalage, ou convertit une date qui en porte déjà un

```
datezone(token, zone)
```

**Exemple**

```jslt
{ "r": datezone($.d, "Europe/Paris") }
```

```json
{ "d": "2026-11-11T09:30:00" }
```

```json
{ "r": "2026-11-11T09:30:00+01:00" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel |  |
| `zone` | optionnel |  |

**Chapitre** : [Dates et heures](../dates.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
