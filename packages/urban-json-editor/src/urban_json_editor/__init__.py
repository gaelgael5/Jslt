"""urban-json-editor — composant d'édition jslt réutilisable (coloration + intellisense).

Fournit un Web Component ``<jslt-editor>`` (assets statiques JS/CSS, sans
dépendance côté navigateur) et de petits utilitaires Python pour l'intégrer dans
n'importe quel projet web Python :

* :func:`assets_dir` — chemin du dossier des assets à servir en statique ;
* :func:`catalog` — catalogue de fonctions (pour l'intellisense) depuis un
  registre jslt ;
* :func:`mount` — monte les assets sur une application FastAPI/Starlette.

Exemple (FastAPI) :

    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    import urban_json_editor

    app = FastAPI()
    urban_json_editor.mount(app, "/jslt-editor")

    @app.get("/api/functions")
    def functions():
        return JSONResponse({"functions": urban_json_editor.catalog()})

puis dans la page :

    <link rel="stylesheet" href="/jslt-editor/jslt-editor.css">
    <script type="module" src="/jslt-editor/jslt-editor.js"></script>
    <jslt-editor catalog-url="/api/functions"></jslt-editor>
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

__version__ = "0.1.1"

__all__ = ["ASSET_FILES", "assets_dir", "catalog", "mount"]

#: Fichiers d'assets livrés par le composant.
ASSET_FILES = ("jslt-editor.js", "jslt-editor.css")


def assets_dir() -> Path:
    """Dossier contenant les assets statiques du composant (JS/CSS)."""
    return Path(__file__).resolve().parent / "static"


def catalog(registry: Any = None) -> list[dict[str, Any]]:
    """Catalogue de fonctions pour l'intellisense (depuis un registre jslt).

    Par défaut, le registre global de ``urban-json`` (fonctions intégrées + plugins
    découverts). Passer un registre dédié pour restreindre les propositions.
    """
    if registry is None:
        from urban_json import default_registry

        registry = default_registry
    return registry.catalog()


def mount(app: Any, url_path: str = "/jslt-editor", name: str = "jslt-editor") -> None:
    """Monte les assets du composant sur une app FastAPI/Starlette à ``url_path``.

    ``fastapi``/``starlette`` n'est pas une dépendance de ce paquet : l'import est
    fait ici, à l'appel. Pour un autre framework, servir :func:`assets_dir` à la
    main.
    """
    from starlette.staticfiles import StaticFiles

    app.mount(url_path, StaticFiles(directory=str(assets_dir())), name=name)
