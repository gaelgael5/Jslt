"""Fonctions de collection (port des ``Services.distinct`` / ``Services.group``).

``select`` et ``selectmany`` reçoivent leur chemin comme argument compilé
(``path_args``), appliqué au document source.
"""

from __future__ import annotations

from typing import Any

from .registry import jslt_function


@jslt_function("limit")
def execute_limit(ctx: Any, source: Any = None, max_items: int = 0) -> Any:
    """Les ``max_items`` premiers éléments d'un tableau (port de ``ExecuteLimit``)."""
    if isinstance(source, list):
        return source[:max_items]
    return None


@jslt_function("union")
def execute_union(ctx: Any, source: Any = None) -> list:
    """Aplatit d'un niveau un tableau de tableaux (port de ``ExecuteUnion``)."""
    result: list = []
    if isinstance(source, list):
        for token in source:
            if isinstance(token, list):
                result.extend(token)
            else:
                result.append(token)
    return result


@jslt_function("select", path_args=(1,))
def execute_select(ctx: Any, source: Any = None, path: Any = None) -> Any:
    """Première valeur sélectionnée par le chemin (port de ``ExecuteSelectOne``)."""
    if source is None or path is None:
        return None
    values = path.select_values(source)
    return values[0] if values else None


@jslt_function("selectmany", path_args=(1,))
def execute_selectmany(ctx: Any, source: Any = None, path: Any = None) -> list:
    """Toutes les valeurs sélectionnées par le chemin (port de ``ExecuteSelectMany``)."""
    if source is None or path is None:
        return []
    return path.select_values(source)
