<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `datediff`

*[Français](datediff.md) · English*

Counts the whole units elapsed between two ISO 8601 dates: second, minute, hour, day, week, month or year, negative when the end precedes the start

```
datediff(start, end, unit)
```

**Examples**

***Whole** elapsed units, negative when the end precedes the start.*

```jslt
{ "jours": datediff($.a, $.b, "day"), "a_rebours": datediff($.b, $.a, "day") }
```

```json
{ "a": "2026-11-01T00:00:00", "b": "2026-11-11T00:00:00" }
```

```json
{ "jours": 10, "a_rebours": -10 }
```

*A month only counts once the end's **day** has caught up with the start's: from 15 January to 14 February there is none.*

```jslt
{ "veille": datediff($.a, $.b, "month"), "jour_meme": datediff($.a, $.c, "month") }
```

```json
{ "a": "2026-01-15T00:00:00", "b": "2026-02-14T00:00:00", "c": "2026-02-15T00:00:00" }
```

```json
{ "veille": 0, "jour_meme": 1 }
```

| Parameter | Expected | Note |
|---|---|---|
| `start` | optional | ISO 8601 start date |
| `end` | optional | ISO 8601 end date; before the start, the result is negative |
| `unit` | optional | `second`, `minute`, `hour`, `day`, `week`, `month` or `year` |

**Good to know**

- The count is in **whole elapsed** units, truncated **towards zero**: from 15 January to 14 February there are `0` months, and to 15 February `1`.
- Comparing a date **with** a timezone to one **without** raises: the difference would be meaningless, and assuming one would be wrong by a few hours.

**Chapter**: [Dates and times](../dates.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
