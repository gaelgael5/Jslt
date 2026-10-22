"""Plugin urban-json : fichiers JSON et chemins (``loadjson``, ``iteratejsonfile``,
``concatpath``).

Port de ``Services.cs`` (``loadjson``, ``IterateJsonFile``) et
``Services.paths.cs`` (``concatpath``) du .NET. Ces fonctions lisent le disque :
elles restent hors du cœur, que le playground exécute en bac à sable.

Découvert automatiquement via l'entry point ``urban_json.functions`` ; aussi
enregistrable à la main : ``from urban_json_files import register``.

Écarts volontaires vs .NET :

* La résolution de chemin du .NET (``ctx.Configuration.ResolveFile``) n'existe pas
  dans le portage : un chemin relatif l'est au répertoire courant (comme
  ``loadcsv``). Le BOM éventuel est ignoré.
* ``iteratejsonfile`` lit le fichier entier puis applique le chemin, au lieu du
  lecteur en flux ``BigJsonReader`` : le .NET matérialisait de toute façon le
  résultat complet (``new JArray(enumerator)``). Le chemin est accepté compilé
  (``$.root.*``) ou en chaîne (``"$.root.*"``, forme du .NET).
* Erreurs (JSON invalide, fichier manquant pour ``iteratejsonfile``) : ``JsltError``
  explicite.
"""

from __future__ import annotations

import json
import os
from typing import Any

from urban_json import JsltError
from urban_json.functions._helpers import as_json_path, to_text

__version__ = "0.1.0"

__all__ = ["execute_concatpath", "execute_iteratejsonfile", "execute_loadjson", "register"]


def _read_json(path: str, function: str) -> Any:
    try:
        with open(path, encoding="utf-8-sig") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise JsltError(f"{function} : JSON invalide dans {path!r} ({exc})") from exc


def execute_loadjson(ctx: Any, source_path: Any = None) -> Any:
    if not source_path:
        raise JsltError("loadjson : le chemin du fichier est requis")
    path = to_text(source_path)
    if not os.path.isfile(path):
        return None  # le .NET émettait un avertissement et rendait null
    return _read_json(path, "loadjson")


def execute_iteratejsonfile(ctx: Any, file_source: Any = None, slicer: Any = None) -> list:
    if not file_source:
        raise JsltError("iteratejsonfile : le chemin du fichier est requis")
    if slicer is None:
        raise JsltError("iteratejsonfile : le chemin JSONPath de découpe est requis")
    path = to_text(file_source)
    if not os.path.isfile(path):
        raise JsltError(f"iteratejsonfile : fichier introuvable {path!r}")
    return as_json_path(slicer).select_values(_read_json(path, "iteratejsonfile"))


def execute_concatpath(ctx: Any, path: Any = None) -> Any:
    if not isinstance(path, list):
        return None
    parts = [to_text(item) for item in path if item is not None]
    # Path.Combine .NET = os.path.join : un segment absolu repart de la racine.
    return os.path.join(*parts) if parts else ""


def register(registry: Any) -> None:
    """Enregistre ``loadjson``, ``iteratejsonfile`` et ``concatpath``."""
    registry.register(
        "loadjson", execute_loadjson,
        description="Lit un fichier JSON et renvoie son contenu (null si le fichier n'existe pas)",
    )
    registry.register(
        "iteratejsonfile", execute_iteratejsonfile, path_args=(1,),
        description="Lit un fichier JSON et renvoie le tableau des éléments sélectionnés par un chemin JSONPath",
    )
    registry.register(
        "concatpath", execute_concatpath,
        description="Assemble un chemin de fichier à partir d'un tableau de segments (null ignorés)",
    )
