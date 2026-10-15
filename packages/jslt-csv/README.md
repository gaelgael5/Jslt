# jslt-csv

Plugin [jslt](https://github.com/gaelgael5/Jslt) : lecture de fichiers **CSV**
dans les templates, via la fonction `loadcsv`. Port de
`Bb.CustomServices.ServiceCsv` (.NET).

## Installation

```bash
pip install jslt-csv      # tire jslt en dépendance
```

Rien d'autre à faire : `jslt` découvre le plugin automatiquement via les entry
points (`jslt.functions`). `loadcsv` devient utilisable dans les templates.

## Utilisation

```python
from jslt import JsltTemplate

# people.csv :
#   name;age;active
#   Alice;30;true
#   Bob;25;false
tpl = JsltTemplate.parse('[ { "$source": loadcsv("people.csv"), "n": $.name, "a": $.age } ]')
tpl.transform({})
# -> [{'n': 'Alice', 'a': 30}, {'n': 'Bob', 'a': 25}]
```

`loadcsv` renvoie un tableau d'objets (une entrée par ligne) ; il s'enchaîne donc
naturellement avec une boucle `$source`, un filtre `?(...)`, etc.

## Signature

```
loadcsv(source_path, has_header=true, separator=";", quote="\"", escape="\\",
        excluded_columns=null, exclude_null_and_empty=false)
```

| Paramètre | Rôle |
|---|---|
| `source_path` | chemin du fichier CSV (absolu ou relatif au répertoire courant) |
| `has_header` | la 1re ligne porte les noms de colonnes (sinon `Column0`, `Column1`…) |
| `separator` | séparateur de champs (défaut `;`) |
| `quote` | caractère de citation (défaut `"`) |
| `escape` | caractère d'échappement (défaut `\`) |
| `excluded_columns` | noms de colonnes à exclure, séparés par `separator` |
| `exclude_null_and_empty` | omet les cellules nulles/vides |

### Typage des valeurs

Les cellules sont coercées comme en .NET : `true`/`false` → booléen,
entiers/décimaux → nombres, le reste → chaîne (les entêtes sont assainis :
accents → ASCII, espaces → `_`).

## Licence

Apache-2.0.
