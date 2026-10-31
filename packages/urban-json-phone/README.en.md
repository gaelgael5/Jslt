# urban-json-phone

*[Français](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-phone/README.md) · English*

[urban-json](https://github.com/gaelgael5/Jslt) plugin: **phone number
validation** through `phoneisvalid(number, region)` (port of the .NET function,
backed by the same libphonenumber library via `phonenumbers`).

```bash
pip install urban-json-phone
```

- `phoneisvalid("+33 6 12 34 56 78", "")` → `true` (international: `+` or `00`);
- `phoneisvalid("06 12 34 56 78", "FR")` → `true` (national, read with the ISO
  region);
- an unreadable or empty number, or a national one without a region → `false`.
