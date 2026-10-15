# jslt-editor

Composant d'édition **jslt** réutilisable : un Web Component `<jslt-editor>` avec
**coloration syntaxique** et **intellisense** (auto-complétion des fonctions),
livré pour être intégré dans n'importe quel projet web Python.

- **Sans dépendance côté navigateur** (vanilla Web Component) → aucun build node,
  drop-in dans un projet existant.
- **Intellisense** alimentée par le catalogue de fonctions de `jslt`
  (`registry.catalog()`), donc toujours à jour — y compris les fonctions de
  plugins installés.

## Installation

```bash
pip install jslt-editor
```

## Intégration (FastAPI)

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import jslt_editor

app = FastAPI()
jslt_editor.mount(app, "/jslt-editor")          # sert les assets JS/CSS

@app.get("/api/functions")
def functions():
    return JSONResponse({"functions": jslt_editor.catalog()})
```

Dans la page :

```html
<link rel="stylesheet" href="/jslt-editor/jslt-editor.css">
<script type="module" src="/jslt-editor/jslt-editor.js"></script>

<jslt-editor id="ed" catalog-url="/api/functions"></jslt-editor>
<script>
  const ed = document.getElementById("ed");
  ed.value = '{ "n": $.x }';
  ed.addEventListener("input", () => console.log(ed.value));
</script>
```

## API Python

| Fonction | Rôle |
|---|---|
| `assets_dir()` | dossier des assets statiques (pour servir à la main, hors FastAPI) |
| `catalog(registry=None)` | catalogue de fonctions (intellisense) depuis un registre jslt |
| `mount(app, url_path="/jslt-editor")` | monte les assets sur une app FastAPI/Starlette |

## API du composant

- Propriété `value` (get/set) — le texte du template (source de vérité).
- `setCatalog(list)` — fournit le catalogue d'intellisense par programme.
- Attribut `catalog-url` — URL d'où charger le catalogue (`{functions:[...]}`).
- Événement `input` — émis à chaque modification.
- Variables CSS `--jslt-ed-*` surchargeables (couleurs, police, hauteur).

## Licence

Apache-2.0.
