# urban-json-files

*Français · [English](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-files/README.en.md)*

Plugin [urban-json](https://github.com/gaelgael5/Jslt) : **fichiers JSON et chemins**
dans les templates (port des fonctions .NET `loadjson`, `IterateJsonFile`, `concatpath`).

```bash
pip install urban-json-files
```

| Fonction | Rôle |
|---|---|
| `loadjson(chemin)` | Contenu d'un fichier JSON (`null` si le fichier n'existe pas). |
| `iteratejsonfile(chemin, "$.chemin")` | Éléments d'un fichier JSON sélectionnés par un JSONPath (compilé ou en chaîne). |
| `concatpath(["dossier", "fichier.json"])` | Chemin de fichier assemblé (`null` ignorés ; un segment absolu repart de la racine). |

```python
from urban_json import JsltTemplate

tpl = JsltTemplate.parse('{ "ids": iteratejsonfile("data.json", "$.items[*].id") }')
tpl.transform({})
```

Les chemins relatifs le sont au répertoire courant. Ces fonctions lisent le disque :
elles ne sont pas disponibles dans le playground (bac à sable du cœur).
