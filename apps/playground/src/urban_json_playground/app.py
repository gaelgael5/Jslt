"""Playground jslt — petite application web de test/démo (FastAPI).

Saisir un template jslt + un document JSON source → voir le résultat transformé
par le **vrai moteur** jslt (côté serveur).

Sécurité : le playground n'exécute que les **fonctions du cœur**. Les plugins
d'E-S (CSV, XML, SQL, HTTP, Elasticsearch) ne sont PAS chargés — sinon un template
arbitraire pourrait lire des fichiers du serveur, émettre des requêtes (SSRF) ou
exécuter du SQL. On passe un registre isolé (copie du registre cœur, capturée à
l'import avant tout chargement de plugin) à chaque transformation.

Lancer en local :

    pip install -e "apps/playground[dev]"
    uvicorn urban_json_playground.app:app --reload
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import urban_json_editor
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from urban_json import JsltError, JsltTemplate, default_registry

# Registre cœur isolé, capturé AVANT tout chargement de plugin (les plugins ne se
# chargent que paresseusement, au 1er transform sur le registre global). Garantit
# un bac à sable : aucune fonction d'E-S accessible depuis un template utilisateur.
_CORE_REGISTRY = default_registry.copy()

# Garde-fous d'entrée (le playground n'est pas durci pour un hébergement public).
_MAX_INPUT = 100_000  # caractères, par champ

_STATIC = Path(__file__).resolve().parent / "static"

app = FastAPI(title="jslt playground", version="0.0.1")

# Assets du composant d'édition réutilisable (coloration + intellisense).
urban_json_editor.mount(app, "/jslt-editor")


class TransformRequest(BaseModel):
    template: str = Field(default="", max_length=_MAX_INPUT)
    source: str = Field(default="null", max_length=_MAX_INPUT)


@app.post("/api/transform")
def transform(req: TransformRequest) -> JSONResponse:
    """Transforme ``source`` (JSON) par ``template`` (jslt) et renvoie le résultat.

    Réponse : ``{"result": <json>}`` ou ``{"error": "..."}`` (HTTP 400).
    """
    try:
        source: Any = json.loads(req.source) if req.source.strip() else None
    except json.JSONDecodeError as exc:
        return JSONResponse({"error": f"JSON source invalide : {exc}"}, status_code=400)

    try:
        result = JsltTemplate.parse(req.template).transform(source, functions=_CORE_REGISTRY)
    except JsltError as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)
    except NotImplementedError as exc:
        return JSONResponse({"error": f"Construction non portée : {exc}"}, status_code=400)
    except Exception as exc:  # noqa: BLE001 — garde-fou : jamais de 500 brut vers l'UI
        return JSONResponse({"error": f"{type(exc).__name__}: {exc}"}, status_code=400)

    return JSONResponse({"result": result})


class DebugRequest(BaseModel):
    template: str = Field(default="", max_length=_MAX_INPUT)
    source: str = Field(default="null", max_length=_MAX_INPUT)
    break_functions: list[str] = Field(default_factory=list)
    break_lines: list[int] = Field(default_factory=list)


@app.post("/api/debug")
def debug(req: DebugRequest) -> JSONResponse:
    """Évalue en mode pas-à-pas : renvoie ``{result, steps, error}``.

    Chaque étape = un nœud évalué (type, localisation, source courante, valeur).
    ``break_functions`` / ``break_lines`` marquent les points d'arrêt.
    """
    try:
        source: Any = json.loads(req.source) if req.source.strip() else None
    except json.JSONDecodeError as exc:
        return JSONResponse({"error": f"JSON source invalide : {exc}"}, status_code=400)

    try:
        result = JsltTemplate.parse(req.template).debug(
            source,
            functions=_CORE_REGISTRY,
            break_functions=req.break_functions,
            break_lines=req.break_lines,
        )
    except JsltError as exc:  # erreur de parsing (avant exécution)
        return JSONResponse({"error": str(exc)}, status_code=400)
    except Exception as exc:  # noqa: BLE001 — garde-fou : jamais de 500 brut vers l'UI
        return JSONResponse({"error": f"{type(exc).__name__}: {exc}"}, status_code=400)

    return JSONResponse(result.to_dict())


@app.get("/api/functions")
def functions() -> JSONResponse:
    """Catalogue des fonctions disponibles (cœur) — pour l'aide de l'éditeur."""
    return JSONResponse({"functions": _CORE_REGISTRY.catalog()})


@app.get("/api/examples")
def examples() -> JSONResponse:
    """Exemples prêts à charger (template + source) couvrant le langage."""
    from .examples import examples as _examples

    return JSONResponse({"examples": _examples()})


@app.get("/")
def index() -> FileResponse:
    return FileResponse(_STATIC / "index.html")
