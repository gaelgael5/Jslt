"""Fonctions de sortie : ``to_json`` / ``to_block`` (port de
``CustomServices/Outputs.cs``), ``to_csv`` / ``to_xml`` / ``to_yaml`` (au-delà du
.NET, émetteurs dans :mod:`._writers`).

Elles ne s'appellent pas dans le corps du template : elles se déclarent dans
``"$directives": {"output": {"mode": to_json(...)}}`` et sont appliquées par
``JsltTemplate.render``. Le résultat à sérialiser est ``ctx.token_result``
(``ctx.TokenResult`` en .NET) ; elles rendent le texte produit.
"""

from __future__ import annotations

import copy
import json
from typing import Any

from ._helpers import to_text
from ._writers import to_csv_text, to_xml_text, to_yaml_text
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
    description_en="Output: serialises the result as JSON, indented when indented is true; ignore_null_and_empty_value drops the null or empty properties",
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
    description_en="Output: one compact JSON line per element of the resulting array (JSON Lines), or the resulting object on one line",
)
def execute_to_block(ctx: Any) -> str:
    value = ctx.token_result
    if isinstance(value, dict):
        return _compact(value) + "\n"
    if isinstance(value, list):
        return "".join(_compact(item) + "\n" for item in value)
    return ""


# --- CSV, XML, YAML -----------------------------------------------------------
# Le moteur lisait trois formats et n'en écrivait qu'un. Les émetteurs sont dans
# `_writers.py` : ce module ne fait que les déclarer au registre.


@jslt_function(
    "to_csv",
    kind="output",
    description="Sortie : le tableau résultat en CSV (séparateur et ligne d'en-tête réglables)",
    description_en="Output: the resulting array as CSV (separator and header row adjustable)",
)
def execute_to_csv(ctx: Any, separator: str = ";", header: bool = True) -> str:
    """Sortie CSV d'un tableau d'objets.

    Le séparateur est ``;`` par défaut, comme ``loadcsv`` à la lecture : les deux
    bouts du dépôt parlent la même langue par défaut.
    """
    return to_csv_text(ctx.token_result, (separator or ";")[0], header)


@jslt_function(
    "to_xml",
    kind="output",
    description="Sortie : le résultat en XML sous l'élément racine donné (@clef = attribut, #text = contenu)",
    description_en="Output: the result as XML under the given root element (@key = attribute, #text = content)",
)
def execute_to_xml(ctx: Any, root: str = "root") -> str:
    return to_xml_text(ctx.token_result, to_text(root))


@jslt_function(
    "to_yaml",
    kind="output",
    description="Sortie : le résultat en YAML, en style bloc ou en style JSON si json_style vaut true",
    description_en="Output: the result as YAML, in block style or in JSON style when json_style is true",
)
def execute_to_yaml(ctx: Any, json_style: bool = False) -> str:
    return to_yaml_text(ctx.token_result, bool(json_style))
