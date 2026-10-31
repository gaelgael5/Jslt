# urban-json-editor

*Français · [English](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-editor/README.en.md)*

Composant d'édition **jslt** réutilisable : un Web Component `<jslt-editor>` avec
**coloration syntaxique** et **intellisense** (fonctions **et chemins du document
source**), livré pour être intégré dans n'importe quel projet web Python.

- **Sans dépendance côté navigateur** (vanilla Web Component) → aucun build node,
  drop-in dans un projet existant. Depuis la 0.2.0 il n'est plus **mono-fichier** :
  `jslt-editor.js` importe `jslt-paths.js` en module, donc les assets doivent être
  **servis** côte à côte (monter `assets_dir()` en statique). Injecter le JS en
  ligne dans la page échoue sur `Failed to resolve module specifier
  "./jslt-paths.js"`, faute de base d'URL.
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

### Pourquoi rien n'est proposé (messages de diagnostic)

Une liste vide voulait dire six choses : une erreur de syntaxe, un segment
inexistant, une boucle qui ne désigne rien, un document source absent… et aussi
« tu es au bon endroit, il n'y a rien dessous ». Le composant sait les
distinguer, et peut le dire là où la liste se serait ouverte.

**Opt-in** : sans l'attribut, le composant reste muet comme en 0.2.x — un
composant qui se met à parler dans tous les projets qui l'utilisent serait une
rupture.

```html
<jslt-editor hints></jslt-editor>          <!-- ou ed.hints = true -->
```

```js
// Les textes sont surchargeables par CODE de cause (le composant ne porte aucun
// dispositif de traduction) ; un code non surchargé garde son texte livré.
ed.setMessages({
  "at-outside-filter": "@ only denotes an element inside a [?(…)] filter",
  "unknown-segment": "{segment} is not in the source document",
});
```

| Code | Situation |
|---|---|
| `no-source-doc` | aucun document source, ou document illisible |
| `at-outside-filter` | `@` hors de tout filtre (`{ "a": @. }`) |
| `at-filter-without-brackets` | `@` dans un `?(…)` **sans crochets** (le moteur refuse) |
| `unknown-segment` | segment absent du document (`$.Inconnu.`) — donnée `{segment}` |
| `loop-source-incomplete` | chemin de `$source` en cours de frappe |
| `loop-source-empty` | `$source` qui ne désigne aucune collection — donnée `{path}` |
| `filter-path-unknown` | collection filtrée non résoluble (`sum($.a)[?(@.`) |
| `filter-path-empty` | collection filtrée introuvable — donnée `{path}` |
| `no-children` | nœud feuille : bon endroit, rien dessous |
| `no-match` | aucune clé ne commence par ce qui est tapé — donnée `{prefix}` |

Le message **ne remplace jamais une liste** : il n'apparaît que si aucune
proposition n'était possible, et il n'apparaît pas hors d'un chemin (il répond à
un geste, il ne commente pas la frappe). Il disparaît à la frappe suivante et à
`Échap`, ne capture aucune touche, et n'interdit rien : l'éditeur informe, il ne
valide pas le template — dire si un template compile reste le travail du moteur.

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
- Attribut `hints` / propriété `hints` (get/set) — active les messages de
  diagnostic (**défaut : désactivé**, aucun message).
- `setMessages(dict)` — textes des messages par code de cause, fusionnés avec
  les défauts (`DEFAULT_HINT_MESSAGES`, exporté par `jslt-paths.js`).
- Attribut `catalog-url` — URL d'où charger le catalogue (`{functions:[...]}`).
- Événement `input` — émis à chaque modification.
- Clavier : tant que la liste de propositions est ouverte, l'éditeur **capture**
  `Tab`, `Enter`, `Escape` et ↑/↓ (`preventDefault`) ; un hôte qui câble `Enter`
  ou `Tab` teste `event.defaultPrevented`. Hors liste ouverte, `Tab` indente de
  deux espaces et les autres touches remontent à l'hôte.
- Variables CSS `--jslt-ed-*` surchargeables (couleurs, police, hauteur).

## Licence

Apache-2.0.
