<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `htmlescape`

*[Français](htmlescape.md) · English*

Escapes the characters that mean something in HTML (< > & " ')

```
htmlescape(token)
```

**Example**

```jslt
{ "r": htmlescape($.t) }
```

```json
{ "t": "<b>ok</b>" }
```

```json
{ "r": "&lt;b&gt;ok&lt;/b&gt;" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Encoding, digests and escaping](../encodage.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
