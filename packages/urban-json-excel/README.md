# urban-json-excel

*Français · [English](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-excel/README.en.md)*

Plugin [urban-json](https://github.com/gaelgael5/Jslt) : **classeurs Excel** dans les
templates (port de `ServicesXls` / `ExcelReader`, .NET).

```bash
pip install urban-json-excel          # .xlsx (openpyxl)
pip install "urban-json-excel[xls]"   # + anciens .xls (xlrd)
```

- `loadxls(classeur, "config.json")` — configuration lue dans un fichier JSON ;
- `loadxlssheet(classeur, { … })` — configuration passée en objet.

```json
{ "FirstRowHasColumnName": true, "HeaderLine": 0, "Tablename": "Feuil1",
  "AddRowNumber": true, "ByPassEmptyObject": true,
  "Columns": [ { "Index": 0, "Name": "id", "Type": "integer", "Trimmed": true, "BypassEmptyValue": true } ] }
```

Chaque ligne devient un objet (`"$row"` = rang de la ligne de données si
`AddRowNumber`). Sans `Columns`, toutes les colonnes sont lues, noms assainis
(`"Nom complet"` → `Nom_complet`) et colonnes entièrement entières typées `integer`.
Si `Tablename` est vide, la feuille unique du classeur est prise.
