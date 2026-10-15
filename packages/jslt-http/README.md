# jslt-http

Plugin [jslt](https://github.com/gaelgael5/Jslt) : appels **HTTP** depuis les
templates. L'appel est formalisé comme un objet **Fetch / `RequestInit`** (le
vocabulaire HTTP-en-JSON standard).

## Installation

```bash
pip install jslt-http      # tire jslt et httpx
```

`jslt` découvre le plugin automatiquement via les entry points (`jslt.functions`).

## Utilisation

```python
from jslt import JsltTemplate

tpl = JsltTemplate.parse('''
{
  "r:": http({
    "method": "GET",
    "url": "https://api.example.com/users",
    "headers": { "Authorization": $.token },
    "query": { "page": 1 }
  }),
  "code": r:$.status,
  "users": r:$.body.items
}
''')
tpl.transform({"token": "Bearer xyz"})
```

- `http(request)` — `request` : `{ method, url, headers, query, body, timeout }`.
  Renvoie `{ status, headers, body }` ; `body` est le JSON parsé si la réponse est
  du JSON, sinon le texte.
- `httpget(url, headers)` — convenance GET renvoyant directement le `body`.

Le corps (`body`) de la requête est envoyé en **JSON** si c'est un objet ou un
tableau, sinon tel quel. Verbe par défaut : `GET`. Timeout par défaut : 30 s
(surchargeable via `"timeout"`).

## Sécurité

`http` réalise de **vraies requêtes réseau**. Méfiez-vous des URL construites à
partir de données non fiables (SSRF). Un timeout par défaut est appliqué.

## Licence

Apache-2.0.
