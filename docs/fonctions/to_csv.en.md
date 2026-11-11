<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `to_csv`

*[Français](to_csv.md) · English*

Output: the resulting array as CSV (separator and header row adjustable)

```
to_csv(separator, header)
```

**Example**

```jslt
{ "$directives": { "output": { "filter": $.lignes, "mode": to_csv() } }, "lignes": [ { "$source": $.clients, "id": $.id, "ville": $.adr.ville } ] }
```

```json
{ "clients": [{ "id": 1, "adr": { "ville": "Lyon" } }] }
```

```json
{ "lignes": [{ "id": 1, "ville": "Lyon" }] }
```

`render()` produces:

```text
id;ville
1;Lyon
```

| Parameter | Expected | Note |
|---|---|---|
| `separator` | optional |  |
| `header` | optional |  |

An **output** function: it is not called in the template body, it is declared in `"$directives": {"output": {"mode": …}}`.

**Chapter**: [Text output](../sortie.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
