# urban-json-random

*[Français](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-random/README.md) · English*

[urban-json](https://github.com/gaelgael5/Jslt) plugin: **random data** in
templates, through the 25 `getrandom_*` functions of the original .NET engine
(port of `Services.randoms.cs`). Useful to produce realistic test data.

## Installation

```bash
pip install urban-json-random      # pulls urban-json, Faker and rstr
```

Nothing else to do: `urban-json` discovers the plugin automatically through the
entry points (`urban_json.functions`).

## Usage

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

## Functions

| Family | Functions |
|---|---|
| Numbers | `getrandom_integer`, `getrandom_long`, `getrandom_short`, `getrandom_byte`, `getrandom_double`, `getrandom_float` — `(minimum, exclusiveMinimum, maximum, exclusiveMaximum)` |
| Text | `getrandom_string(min_length, max_length, pattern)`, `getrandom_lipsum(paragraphs)`, `getrandom_password(token, length)`, `getrandom_naughtystrings()` |
| People | `getrandom_firstname`, `getrandom_lastname`, `getrandom_fullname`, `getrandom_email` |
| Places | `getrandom_city`, `getrandom_country` |
| Network | `getrandom_ipv4`, `getrandom_ipv6`, `getrandom_macaddress(minimum, maximum)` |
| Banking | `getrandom_iban(country, include_iban, include_bban)` |
| Time | `getrandom_datatime()` (original name kept), `getrandom_timespan()` |
| Misc | `getrandom_boolean()`, `getrandom_binary(min_length, max_length)`, `getrandom_in_list(items)` |

## Deliberate deviations from .NET

- `exclusiveMinimum` / `exclusiveMaximum` exclude the bound (JSON Schema
  meaning); .NET widened the interval instead.
- Without bounds: the full range of the type (`integer` 0 to 2³¹−1, `double` in
  [0, 1)…); .NET often returned 0 every time.
- Impossible interval: explicit `JsltError`.
- `getrandom_boolean` and `getrandom_in_list` draw for real (.NET used the
  parity of the current milliseconds); an empty list gives `null`.
- `getrandom_password` uses a cryptographic generator (`secrets`).
- Dates and durations as text: ISO 8601 and `hh:mm:ss.fff`.
