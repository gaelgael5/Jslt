# urban-json-csv

Plugin [urban-json](https://github.com/gaelgael5/Jslt) : lecture de fichiers **CSV**
dans les templates, via la fonction `loadcsv`. Port de
`Bb.CustomServices.ServiceCsv` (.NET).

## Installation

```bash
pip install urban-json-csv      # tire urban-json en dépendance
```

Rien d'autre à faire : `urban-json` découvre le plugin automatiquement via les entry
points (`urban_json.functions`). `loadcsv` devient utilisable dans les templates.

## Utilisation

```python
from urban_json import JsltTemplate

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

## `loadmcsv` — CSV multi-enregistrements hiérarchique

Port de `ServicesMultiCsv` : un fichier `;`-délimité où chaque ligne est préfixée
par un **type d'enregistrement**, les colonnes de chaque type étant déclarées par
des lignes `#DEF`. Un `rule_payload` décrit la **hiérarchie**.

```
#DEF;CATALOG;id;name
#DEF;BOOK;code;title
CATALOG;1;Librairie
BOOK;a;Alpha
BOOK;b;Beta
#END
```

```python
from urban_json import JsltTemplate
JsltTemplate.parse(
    '[ { "$source": selectmany(loadmcsv("catalog.mcsv", "CATALOG:BOOK"), $.BOOK.*), "t": $.title } ]'
).transform({})
# -> [{'t': 'Alpha'}, {'t': 'Beta'}]
```

`loadmcsv(source_path, rule_payload, encoding, ignore_empty)` :
- `rule_payload` : règles `"PARENT:ENF1|ENF2; …"` (séparées par `;`). Un bloc dont
  le nom est enfant du parent courant s'y imbrique, sinon il remonte.
- Les enfants homonymes deviennent un **tableau** ; chaque racine porte un objet
  `_metadatas` (nom de fichier, encodage, métadonnées `#clé` du fichier).
- Lignes `#DEF;<schema>:<NOM>;col…` (colonnes), `#clé;…` (métadonnée), `#END` (fin).

Écarts assumés vs .NET : lecture `utf-8` ; mappage des colonnes par position
tolérant au `;` final (le .NET l'exige) ; noms de types comparés en majuscules.

## Licence

Apache-2.0.
