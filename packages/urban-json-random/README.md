# urban-json-random

*Français · [English](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-random/README.en.md)*

Plugin [urban-json](https://github.com/gaelgael5/Jslt) : **données aléatoires** dans
les templates, via les 25 fonctions `getrandom_*` du moteur .NET d'origine (port de
`Services.randoms.cs`). Utile pour produire des jeux de test réalistes.

## Installation

```bash
pip install urban-json-random      # tire urban-json, Faker et rstr
```

Rien d'autre à faire : `urban-json` découvre le plugin automatiquement via les entry
points (`urban_json.functions`).

## Utilisation

```python
from urban_json import JsltTemplate

tpl = JsltTemplate.parse("""{
  "id": getrandom_integer(1, false, 1000, false),
  "client": getrandom_fullname(),
  "email": getrandom_email(),
  "iban": getrandom_iban("FR"),
  "ref": getrandom_string(0, 0, "^[A-Z]{3}-\\\\d{4}$")
}""")
tpl.transform({})
# -> {'id': 417, 'client': 'Jane Doe', 'email': '…', 'iban': 'FR76…', 'ref': 'QZT-0381'}
```

## Fonctions

| Famille | Fonctions |
|---|---|
| Nombres | `getrandom_integer`, `getrandom_long`, `getrandom_short`, `getrandom_byte`, `getrandom_double`, `getrandom_float` — `(minimum, exclusiveMinimum, maximum, exclusiveMaximum)` |
| Texte | `getrandom_string(min_length, max_length, pattern)`, `getrandom_lipsum(paragraphs)`, `getrandom_password(token, length)`, `getrandom_naughtystrings()` |
| Personnes | `getrandom_firstname`, `getrandom_lastname`, `getrandom_fullname`, `getrandom_email` |
| Lieux | `getrandom_city`, `getrandom_country` |
| Réseau | `getrandom_ipv4`, `getrandom_ipv6`, `getrandom_macaddress(minimum, maximum)` |
| Banque | `getrandom_iban(pays, include_iban, include_bban)` |
| Temps | `getrandom_datatime()` (nom d'origine conservé), `getrandom_timespan()` |
| Divers | `getrandom_boolean()`, `getrandom_binary(min_length, max_length)`, `getrandom_in_list(items)` |

## Écarts volontaires avec le .NET

- `exclusiveMinimum` / `exclusiveMaximum` excluent la borne (sens JSON Schema) ; le
  .NET élargissait au contraire l'intervalle.
- Sans bornes : étendue du type (`integer` 0 à 2³¹−1, `double` dans [0, 1)…) ; le .NET
  générait souvent toujours 0.
- Intervalle impossible : erreur `JsltError` explicite.
- `getrandom_boolean` et `getrandom_in_list` font un vrai tirage (le .NET prenait la
  parité des millisecondes) ; liste vide → `null`.
- `getrandom_password` utilise un générateur cryptographique (`secrets`).
- Dates et durées en texte : ISO 8601 et `hh:mm:ss.fff`.
