<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. Modifier la description dans le registre, pas ici. -->

# `htmlunescape`

*[Français](htmlunescape.md) · English*

Replaces HTML entities (&amp;, &lt;…) with their characters

```
htmlunescape(token)
```

**Example**

```jslt
{ "r": htmlunescape($.t) }
```

```json
{ "t": "&lt;b&gt;ok&lt;/b&gt;" }
```

```json
{ "r": "<b>ok</b>" }
```

| Parameter | Expected | Note |
|---|---|---|
| `token` | optional |  |

**Chapter**: [Encoding, digests and escaping](../encodage.en.md) · **Index**: [all functions](sommaire.en.md)

---

[← jslt guide](../guide.en.md)
