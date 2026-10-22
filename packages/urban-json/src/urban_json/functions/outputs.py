"""Fonctions de sortie ``to_json`` / ``to_block`` (port de ``CustomServices/Outputs.cs``).

Elles ne s'appellent pas dans le corps du template : elles se déclarent dans
``"$directives": {"output": {"mode": to_json(...)}}`` et sont appliquées par
``JsltTemplate.render``. Le résultat à sérialiser est ``ctx.token_result``
(``ctx.TokenResult`` en .NET) ; elles rendent le texte produit.
"""

from __future__ import annotations

import copy
import json
from typing import Any

from .registry import jslt_function


def _compact(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _remove_null_and_empty(token: Any) -> Any:
    """Port du ``JsonVisitor`` .NET : chaîne vide -> null, puis propriétés nulles
    retirées des objets. Les tableaux gardent leurs éléments (devenus null)."""
    if isinstance(token, dict):
        for key in list(token):
            value = token[key]
            if value == "":
                value = None
            else:
                _remove_null_and_empty(value)
            if value is None:
                del token[key]
    elif isinstance(token, list):
        for index, item in enumerate(token):
            if item == "":
                token[index] = None
            else:
                _remove_null_and_empty(item)
    return token


@jslt_function(
    "to_json",
    kind="output",
    description="Sortie : sérialise le résultat en JSON, indenté si indented vaut true ; "
    "ignore_null_and_empty_value retire les propriétés nulles ou vides",
)
def execute_to_json(ctx: Any, indented: bool = False, ignore_null_and_empty_value: bool = False) -> str:
    value = ctx.token_result
    if ignore_null_and_empty_value:
        value = None if value == "" else _remove_null_and_empty(copy.deepcopy(value))
    if indented:
        return json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    return _compact(value) + "\n"


@jslt_function(
    "to_block",
    kind="output",
    description="Sortie : une ligne JSON compacte par élément du tableau résultat "
    "(JSON Lines), ou l'objet résultat sur une ligne",
)
def execute_to_block(ctx: Any) -> str:
    value = ctx.token_result
    if isinstance(value, dict):
        return _compact(value) + "\n"
    if isinstance(value, list):
        return "".join(_compact(item) + "\n" for item in value)
    return ""
