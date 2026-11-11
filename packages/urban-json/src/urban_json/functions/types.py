"""Types, repli sur erreur et lecture de JSON : ``typeof``, ``isarray`` et
compagnie, ``trydefault``, ``parsejson``.

Sans contrepartie .NET. Le langage ne savait interroger une valeur que par
``isnull`` / ``isnotnull`` : impossible de distinguer un tableau d'un objet, donc
impossible d'écrire un template qui s'adapte à une donnée polymorphe (un champ
tantôt scalaire, tantôt liste — cas banal des exports hérités).
"""

from __future__ import annotations

import json
from typing import Any

from urban_json.errors import JsltError

from ._helpers import is_number
from .registry import jslt_function


def type_name(value: Any) -> str:
    """Nom de type JSON d'une valeur (vocabulaire de JSON Schema)."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"  # avant les nombres : un booléen est un int en Python
    if is_number(value):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    return "object"


@jslt_function(
    "typeof",
    description="Type JSON d'une valeur : null, boolean, number, string, array ou object",
    description_en="JSON type of a value: null, boolean, number, string, array or object",
)
def execute_typeof(ctx: Any, token: Any = None) -> str:
    return type_name(token)


@jslt_function("isarray", description="Vrai si la valeur est un tableau JSON", description_en="True when the value is a JSON array")
def execute_isarray(ctx: Any, token: Any = None) -> bool:
    return isinstance(token, list)


@jslt_function("isobject", description="Vrai si la valeur est un objet JSON", description_en="True when the value is a JSON object")
def execute_isobject(ctx: Any, token: Any = None) -> bool:
    return isinstance(token, dict)


@jslt_function("isstring", description="Vrai si la valeur est une chaîne de caractères", description_en="True when the value is a string")
def execute_isstring(ctx: Any, token: Any = None) -> bool:
    return isinstance(token, str)


@jslt_function("isnumber", description="Vrai si la valeur est un nombre (un booléen n'en est pas un)", description_en="True when the value is a number (a boolean is not one)")
def execute_isnumber(ctx: Any, token: Any = None) -> bool:
    return is_number(token)


@jslt_function("isboolean", description="Vrai si la valeur est un booléen (true ou false)", description_en="True when the value is a boolean (true or false)")
def execute_isboolean(ctx: Any, token: Any = None) -> bool:
    return isinstance(token, bool)


@jslt_function(
    "trydefault",
    lazy_args=(0, 1),
    description="Valeur de l'expression, ou celle du repli si l'expression lève une erreur",
    description_en="Value of the expression, or that of the fallback when the expression raises an error",
)
def execute_trydefault(ctx: Any, expression: Any = None, fallback: Any = None) -> Any:
    """Repli sur erreur — ce que ``??`` ne couvre pas.

    ``??`` traite la valeur **absente** ; ici c'est l'expression qui **échoue**
    (division par zéro, cast impossible, fonction qui refuse ses données). Les
    deux arguments sont paresseux : le repli n'est évalué que s'il sert.

    Seules les ``JsltError`` sont rattrapées. Une ``NotImplementedError`` passe :
    elle signale une construction non portée, c'est-à-dire un trou du moteur, et
    la rattraper la ferait passer pour un cas limite de données.
    """
    if expression is None:
        return None
    try:
        return expression()
    except JsltError:
        return None if fallback is None else fallback()


@jslt_function(
    "parsejson",
    description="Lit un texte JSON et rend la valeur correspondante (objet, tableau ou scalaire)",
    description_en="Reads JSON text and returns the matching value (object, array or scalar)",
)
def execute_parsejson(ctx: Any, token: Any = None) -> Any:
    """Ouvre une chaîne qui **contient** du JSON.

    ``to_json`` est une fonction de sortie, refusée dans le corps du template :
    il n'existait donc aucun chemin de retour. Un texte invalide **lève** plutôt
    que de rendre ``null`` — sinon un flux dont la charge utile est corrompue
    produirait un résultat vide, découvert loin de la cause.
    """
    if token is None:
        return None
    if not isinstance(token, str):
        raise JsltError(f"parsejson attend un texte JSON, reçu : {token!r}")
    try:
        return json.loads(token)
    except ValueError as exc:
        raise JsltError(f"JSON invalide : {exc}") from exc
