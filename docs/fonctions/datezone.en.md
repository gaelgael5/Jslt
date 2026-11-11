<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datezone`

*[Français](datezone.md) · English*

Attaches a timezone to a date without offset, or converts a date that already carries one

```
datezone(token, zone)
```

**Example**

*On a date **without** an offset, the timezone is attached: the displayed time does not move. On one that carries an offset, it is converted: this time the **instant** does not move.*

```jslt
{ "attribue": datezone($.a, "Europe/Paris"), "converti": datezone($.b, "UTC") }
```

```json
{ "a": "2026-11-11T09:30:00", "b": "2026-11-11T09:30:00+01:00" }
```

```json
{ "attribue": "2026-11-11T09:30:00+01:00", "converti": "2026-11-11T08:30:00+00:00" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional | the ISO 8601 date |
| `zone` | optional | IANA name (`Europe/Paris`), `UTC`/`Z`, or a fixed offset (`+02:00`) |

**Good to know**

- On a date **without** an offset, the timezone is **attached** (the date does not move); on one that carries an offset, the date is **converted** (the instant does not move). IANA names (`Europe/Paris`), `UTC`, or a fixed offset (`+02:00`).

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
