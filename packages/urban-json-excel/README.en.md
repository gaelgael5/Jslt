# urban-json-excel

*[Français](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-excel/README.md) · English*

[urban-json](https://github.com/gaelgael5/Jslt) plugin: **Excel workbooks** in
templates (port of .NET's `ServicesXls` / `ExcelReader`).

```bash
pip install urban-json-excel          # .xlsx (openpyxl)
pip install "urban-json-excel[xls]"   # + legacy .xls (xlrd)
```

- `loadxls(workbook, "config.json")` — configuration read from a JSON file;
- `loadxlssheet(workbook, { … })` — configuration passed as an object.

```json
{ "FirstRowHasColumnName": true, "HeaderLine": 0, "Tablename": "Sheet1",
  "AddRowNumber": true, "ByPassEmptyObject": true,
  "Columns": [ { "Index": 0, "Name": "id", "Type": "integer", "Trimmed": true, "BypassEmptyValue": true } ] }
```

Every row becomes an object (`"$row"` = rank of the data row when
`AddRowNumber`). Without `Columns`, all columns are read, names are sanitised
(`"Full name"` → `Full_name`) and all-integer columns are typed `integer`. When
`Tablename` is empty, the workbook's single sheet is used.
