"""Fonctions de collection (port des ``Services.distinct`` / ``Services.group``).

``select`` et ``selectmany`` reçoivent leur chemin comme argument compilé
(``path_args``), appliqué au document source.
"""

from __future__ import annotations

from typing import Any

from ._helpers import as_json_path
from .registry import jslt_function


@jslt_function("limit", description="Les max_items premiers éléments d'un tableau")
def execute_limit(ctx: Any, source: Any = None, max_items: int = 0) -> Any:
    """Les ``max_items`` premiers éléments d'un tableau (port de ``ExecuteLimit``)."""
    if isinstance(source, list):
        return source[:max_items]
    return None


@jslt_function("union", description="Aplatit d'un niveau un tableau de tableaux")
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


@jslt_function("select", path_args=(1,), description="Première valeur sélectionnée par un chemin JSONPath dans la source, ou null")
def execute_select(ctx: Any, source: Any = None, path: Any = None) -> Any:
    """Première valeur sélectionnée par le chemin (port de ``ExecuteSelectOne``)."""
    path = as_json_path(path)
    if source is None or path is None:
        return None
    values = path.select_values(source)
    return values[0] if values else None


@jslt_function("selectmany", path_args=(1,), description="Toutes les valeurs sélectionnées par un chemin JSONPath dans la source")
def execute_selectmany(ctx: Any, source: Any = None, path: Any = None) -> list:
    """Toutes les valeurs sélectionnées par le chemin (port de ``ExecuteSelectMany``)."""
    path = as_json_path(path)
    if source is None or path is None:
        return []
    return path.select_values(source)


@jslt_function("any", description="Vrai si la source est un tableau non vide")
def execute_any(ctx: Any, source: Any = None) -> bool:
    # Port de ExecuteAny : seul un tableau compte, un objet ou une chaîne donnent faux.
    return isinstance(source, list) and len(source) > 0


@jslt_function("contains", description="Vrai si le tableau contient un élément égal à la valeur")
def execute_contains(ctx: Any, source: Any = None, to_match: Any = None) -> bool:
    # Égalité de l'opérateur == du langage (comme le .NET, qui passe par
    # EvaluateBinaryOperator) : "2" == 2 est vrai côté chaîne.
    # Import différé : le runtime importe lui-même le registre des fonctions.
    from urban_json.ast import OperationEnum
    from urban_json.runtime.operators import apply_binary

    if not isinstance(source, list):
        return False
    return any(apply_binary(item, OperationEnum.EQUAL, to_match) is True for item in source)


@jslt_function(
    "selectany",
    path_args=(1,),
    description="Vrai si le chemin JSONPath sélectionne au moins une valeur dans la source",
)
def execute_selectany(ctx: Any, source: Any = None, path: Any = None) -> bool:
    path = as_json_path(path)
    if source is None or path is None:
        return False
    # Nœuds sélectionnés, pas valeurs vraies : une valeur 0 ou "" trouvée compte.
    return len(path.evaluate(source)) > 0
