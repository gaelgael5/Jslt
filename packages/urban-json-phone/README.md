# urban-json-phone

Plugin [urban-json](https://github.com/gaelgael5/Jslt) : **validation de numéros de
téléphone** via `phoneisvalid(numéro, région)` (port du .NET, même bibliothèque
libphonenumber grâce à `phonenumbers`).

```bash
pip install urban-json-phone
```

- `phoneisvalid("+33 6 12 34 56 78", "")` → `true` (international : `+` ou `00`) ;
- `phoneisvalid("06 12 34 56 78", "FR")` → `true` (national, lu avec la région ISO) ;
- numéro illisible, vide ou national sans région → `false`.
