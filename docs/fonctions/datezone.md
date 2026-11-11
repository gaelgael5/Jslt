<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datezone`

*Français · [English](datezone.en.md)*

Attribue un fuseau à une date sans décalage, ou convertit une date qui en porte déjà un

```
datezone(token, zone)
```

**Exemple**

*Sur une date **sans** décalage, le fuseau est attribué : l'heure affichée ne bouge pas. Sur une date qui en porte un, elle est convertie : c'est l'**instant** qui ne bouge pas.*

```jslt
{ "attribue": datezone($.a, "Europe/Paris"), "converti": datezone($.b, "UTC") }
```

```json
{ "a": "2026-11-11T09:30:00", "b": "2026-11-11T09:30:00+01:00" }
```

```json
{ "attribue": "2026-11-11T09:30:00+01:00", "converti": "2026-11-11T08:30:00+00:00" }
```

| Paramètre | Attendu | Note |
|---|---|---|
| `token` | optionnel | la date ISO 8601 |
| `zone` | optionnel | nom IANA (`Europe/Paris`), `UTC`/`Z`, ou décalage fixe (`+02:00`) |

**À savoir**

- Sur une date **sans** décalage, le fuseau est **attribué** (la date ne bouge pas) ; sur une date qui en porte un, elle est **convertie** (l'instant ne bouge pas). Noms IANA (`Europe/Paris`), `UTC`, ou décalage fixe (`+02:00`).

**Chapitre** : [Dates et heures](../dates.md) · **Index** : [toutes les fonctions](sommaire.md)

---

[← Guide jslt](../guide.md)
