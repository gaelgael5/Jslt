# urban-json-editor

Composant d'édition **jslt** réutilisable : un Web Component `<jslt-editor>` avec
**coloration syntaxique** et **intellisense** (fonctions **et chemins du document
source**), livré pour être intégré dans n'importe quel projet web Python.

- **Sans dépendance côté navigateur** (vanilla Web Component) → aucun build node,
  drop-in dans un projet existant.
- **Intellisense des fonctions** alimentée par le catalogue de `urban-json`
  (`registry.catalog()`), donc toujours à jour — y compris les fonctions de
  plugins installés.
- **Intellisense des chemins** alimentée soit par le **document source**
  (propriété `source` : les clés réellement présentes, avec leur type et un
  aperçu de leur valeur), soit par la **liste de chemins calculée par
  l'application hôte** (`setPaths` / attribut `paths-url`) quand celle-ci connaît
  son modèle d'entrée sans en avoir d'instance. Le composant ne lit aucun schéma :
  il replie ce qu'on lui donne.

## Installation

```bash
pip install urban-json-editor
```

## Intégration (FastAPI)

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import urban_json_editor

app = FastAPI()
urban_json_editor.mount(app, "/jslt-editor")          # sert les assets JS/CSS

@app.get("/api/functions")
def functions():
    return JSONResponse({"functions": urban_json_editor.catalog()})
```

Dans la page :

```html
<link rel="stylesheet" href="/jslt-editor/jslt-editor.css">
<script type="module" src="/jslt-editor/jslt-editor.js"></script>

<jslt-editor id="ed" catalog-url="/api/functions"></jslt-editor>
<script>
  const ed = document.getElementById("ed");
  ed.value = '{ "n": $.x }';
  ed.source = '{ "x": 1 }';   // document source -> complétion des chemins
  ed.addEventListener("input", () => console.log(ed.value));
</script>
```

## Complétion des chemins

Deux façons d'alimenter les propositions, un seul moteur de complétion :

```js
ed.source = '{ "Account": [{ "Name": "ACME" }] }';   // un document source
// ou, quand l'hôte calcule les chemins depuis son modèle d'entrée :
ed.setPaths([
  "$.Account[0].PickupReference",
  { path: "$.Account[0].Name", type: "string", description: "raison sociale" },
]);
// ou encore, chargés par le composant :
// <jslt-editor paths-url="/api/source-paths"></jslt-editor>   -> {paths:[…]} ou [...]
```

Les chemins de l'hôte **priment** sur le document quand les deux sont fournis
(ils décrivent le modèle, là où un document n'en est qu'une instance). Un JSON
source invalide, une liste vide ou absente : aucune proposition de chemin, les
fonctions restent proposées. Déclencheurs :

| Frappe | Propositions |
|---|---|
| `$`, `$.`, `$.user.` | clés de l'objet atteint |
| `$.items.` | clés des éléments, **préfixées de `[*]`** (`$.items.name` vaut `null` dans le moteur) |
| `$.items[` | `[*]`, `[0]`, `[1]`… (ou les clés, pour un objet) |
| `$..` | clés à toute profondeur |
| `@.` dans un filtre `[?(…)]` | clés de l'élément filtré |
| `$.` dans une boucle `{ "$source": … }` | clés de l'**élément** itéré, pas de la racine |

Chaque proposition affiche le type et un aperçu de la valeur (`objet · 3 clés`,
`texte · "Alice"`…) — ou le type **déclaré** par l'hôte (`string · raison
sociale`), à défaut `valeur`. Les sous-scripts ne sont jamais inventés : une
liste qui ne contient que `$.Account[0]` ne fait pas proposer `[1]`. Une clé qui n'est pas un identifiant s'insère en forme
crochets (`$.user["ville natale"]`). Aucune fonction n'est proposée à l'intérieur
d'un chemin, et aucune clé n'est proposée si le chemin ne se résout pas : mieux
vaut rien qu'une proposition fausse.

## API Python

| Fonction | Rôle |
|---|---|
| `assets_dir()` | dossier des assets statiques (pour servir à la main, hors FastAPI) |
| `catalog(registry=None)` | catalogue de fonctions (intellisense) depuis un registre urban-json |
| `mount(app, url_path="/jslt-editor")` | monte les assets sur une app FastAPI/Starlette |

Les assets sont `jslt-editor.js`, `jslt-paths.js` (importé par le premier) et
`jslt-editor.css` : à servir côte à côte (`ASSET_FILES`).

## API du composant

- Propriété `value` (get/set) — le texte du template (source de vérité).
- Propriété `source` (get/set) / `setSource(doc)` — document source (objet,
  tableau ou texte JSON) d'où sont tirés les chemins proposés.
- Propriété `paths` (get/set) / `setPaths(list)` — chemins calculés par l'hôte :
  `"$.a[0].b"` ou `{path, type, description}`. Priment sur `source`.
- Attribut `paths-url` — URL d'où charger ces chemins (`{paths:[…]}` ou `[…]`).
- `setCatalog(list)` — fournit le catalogue d'intellisense par programme.
- Attribut `catalog-url` — URL d'où charger le catalogue (`{functions:[...]}`).
- Événement `input` — émis à chaque modification.
- Variables CSS `--jslt-ed-*` surchargeables (couleurs, police, hauteur).

## Licence

Apache-2.0.
