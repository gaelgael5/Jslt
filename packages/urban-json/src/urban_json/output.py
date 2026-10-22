"""Directive de sortie ``$directives.output`` (port de ``JsltDirectives`` /
``ScriptBuilderVisitor.ParseDirectives`` / ``JsltTemplate.ApplyOutput`` du .NET).

Un template peut déclarer, dans un objet, la clé ``$directives`` ::

    "$directives": {
      "output": {
        "filter": $.datas,        // optionnel : JSONPath appliqué au résultat
        "mode":   to_json(true)   // obligatoire : fonction de sortie (kind "output")
      }
    }

La directive n'est jamais émise dans le résultat de ``transform`` ;
:meth:`urban_json.JsltTemplate.render` l'applique pour produire un texte. Seule la clé
``output`` est interprétée ; les autres clés .NET (``culture``, ``packages``,
``assemblies``, ``imports``) sont ignorées. La clé ``write`` (fonctions d'écriture
comme ``to_file``) n'est pas portée.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from urban_json.ast import JsltConstant, JsltFunctionCall, JsltObject, JsltPath
from urban_json.errors import JsltError, JsltSemanticError

#: Clé de la directive (comparée sans tenir compte de la casse, comme le .NET).
DIRECTIVES_KEY = "$directives"


@dataclass(frozen=True)
class OutputConfiguration:
    """Configuration de sortie lue dans ``$directives.output``."""

    #: Appel de la fonction de sortie (``mode``), arguments non évalués.
    mode: JsltFunctionCall
    #: Chemin appliqué au résultat avant la sortie (``filter``), ou ``None``.
    filter: Any = None


def parse_output_directive(directives: JsltObject | None) -> OutputConfiguration | None:
    """Lit la configuration ``output`` d'un objet ``$directives`` (``None`` si absente).

    Raises:
        JsltSemanticError: ``output`` mal formé (``mode`` absent ou non fonction,
            ``filter`` qui n'est pas un chemin).
        NotImplementedError: clé ``write`` (fonctions d'écriture non portées).
    """
    if directives is None:
        return None
    output = next((p for p in directives.properties if p.name.lower() == "output"), None)
    if output is None:
        return None
    if not isinstance(output.value, JsltObject):
        raise JsltSemanticError("'$directives.output' attend un objet", location=output.location)

    mode: JsltFunctionCall | None = None
    path: Any = None
    for prop in output.value.properties:
        key = prop.name.lower()
        if key == "mode":
            if not isinstance(prop.value, JsltFunctionCall):
                raise JsltSemanticError(
                    "'mode' attend une fonction de sortie, p.ex. to_json() ou to_block()",
                    location=prop.location,
                )
            mode = prop.value
        elif key == "filter":
            path = _filter_path(prop)
        elif key == "write":
            raise NotImplementedError(
                "'$directives.output.write' : les fonctions d'écriture (to_file…) ne sont pas portées"
            )
        # autre clé : ignorée (le .NET émettait un avertissement)
    if mode is None:
        raise JsltSemanticError(
            "'$directives.output' exige la propriété 'mode' (p.ex. to_json(), to_block())",
            location=output.location,
        )
    return OutputConfiguration(mode=mode, filter=path)


def _filter_path(prop: Any) -> Any:
    from urban_json.functions._helpers import as_json_path

    value = prop.value
    if isinstance(value, JsltPath) and value.variable is None:
        return value.compiled
    if isinstance(value, JsltConstant) and isinstance(value.value, str):
        try:
            return as_json_path(value.value)
        except JsltError as exc:
            raise JsltSemanticError(str(exc), location=prop.location) from exc
    raise JsltSemanticError("'filter' attend un chemin JSONPath, p.ex. $.datas", location=prop.location)


def select_output(path: Any, result: Any) -> Any:
    """Applique ``filter`` comme le .NET : 1 nœud -> ce nœud, plusieurs -> tableau,
    aucun -> ``null``."""
    selected = path.select_values(result)
    if len(selected) == 1:
        return selected[0]
    return selected or None
