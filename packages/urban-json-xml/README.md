# urban-json-xml

*Français · [English](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-xml/README.en.md)*

Plugin [urban-json](https://github.com/gaelgael5/Jslt) : lecture de fichiers **XML**
dans les templates, via la fonction `loadxml`. Suit les conventions XML↔JSON du
`XmlNodeConverter` (.NET/Newtonsoft).

## Installation

```bash
pip install urban-json-xml      # tire urban-json et defusedxml en dépendances
```

`urban-json` découvre le plugin automatiquement via les entry points (`urban_json.functions`) :
`loadxml` devient utilisable dans les templates.

## Utilisation

```python
from urban_json import JsltTemplate

# catalog.xml :
#   <catalog>
#     <book id="1"><title>A</title></book>
#     <book id="2"><title>B</title></book>
#   </catalog>
tpl = JsltTemplate.parse('[ { "$source": select(loadxml("catalog.xml"), $.catalog.book), "t": $.title } ]')
tpl.transform({})
# -> [{'t': 'A'}, {'t': 'B'}]
```

`loadxml` renvoie un objet ; on navigue dedans avec `select`/`selectmany` (fonctions
du cœur) avant d'alimenter une boucle `$source`, un filtre `?(...)`, etc.

## Conventions de conversion XML ↔ JSON

| XML | JSON |
|---|---|
| `<a>v</a>` | `{"a": "v"}` |
| `<a x="1">v</a>` | `{"a": {"@x": "1", "#text": "v"}}` |
| `<a/>` | `{"a": null}` |
| `<a><b>1</b><b>2</b></a>` | `{"a": {"b": ["1", "2"]}}` (frères homonymes → tableau) |

- Attributs → propriétés préfixées par `@`.
- Texte d'un élément mixte → clé `#text`.
- Les valeurs restent des **chaînes** : aucune coercition de type.

## Signature

```
loadxml(source_path, attribute_prefix="@", text_key="#text", strip_namespaces=true)
```

| Paramètre | Rôle |
|---|---|
| `source_path` | chemin du fichier XML |
| `attribute_prefix` | préfixe des propriétés issues d'attributs (défaut `@`) |
| `text_key` | clé portant le texte d'un élément mixte (défaut `#text`) |
| `strip_namespaces` | réduit `{uri}local` au nom local (défaut `true`) |

### Depuis une chaîne : `parsexml`

```
parsexml(texte, attribute_prefix="@", text_key="#text", strip_namespaces=true)
```

Même conversion, mais sur un XML **déjà en main** : colonne d'une base, charge
utile d'un message, réponse HTTP. `loadxml` n'ouvre qu'un fichier, ce qui
obligeait à écrire sur disque pour traiter un XML reçu. `null` reste `null`, et
un XML invalide lève `JsltError` — la famille d'erreurs du moteur, donc
rattrapable par `trydefault` dans le template.

## Sécurité

Le XML est analysé avec [`defusedxml`](https://pypi.org/project/defusedxml/) :
entités externes et expansion d'entités désactivées (protection XXE /
« billion laughs »).

## Licence

Apache-2.0.
