"""Objets : ``keys``, ``values``, ``entries``, ``fromentries``, ``merge``,
``pick``, ``omit``, ``has``, ``renamekeys``.

Sans contrepartie .NET. Le langage ne savait construire un objet que clé par
clé, littéralement : un document dont les clés ne sont connues qu'à l'exécution
(un dictionnaire de tarifs, des colonnes variables) n'était pas traitable.

Convention de la famille : ``null`` et une valeur qui n'est pas un objet donnent
``null`` — un tableau n'est pas « un objet sans clés », c'est une autre forme, et
rendre ``{}`` laisserait croire à un objet vide.
"""

from __future__ import annotations

import copy
from typing import Any

from urban_json.errors import JsltError

from ._helpers import coerce_bool, to_text
from .registry import jslt_function


def _as_object(value: Any) -> dict | None:
    return value if isinstance(value, dict) else None


@jslt_function("keys", description="Clés d'un objet, dans l'ordre du document (null si ce n'est pas un objet)")
def execute_keys(ctx: Any, token: Any = None) -> Any:
    obj = _as_object(token)
    return None if obj is None else list(obj.keys())


@jslt_function("values", description="Valeurs d'un objet, dans l'ordre du document (null si ce n'est pas un objet)")
def execute_values(ctx: Any, token: Any = None) -> Any:
    obj = _as_object(token)
    return None if obj is None else list(obj.values())


@jslt_function(
    "entries",
    description="Paires d'un objet en tableau de { key, value }, dans l'ordre du document",
)
def execute_entries(ctx: Any, token: Any = None) -> Any:
    """Objet -> tableau de ``{key, value}``.

    Des objets nommés plutôt que des paires ``[clé, valeur]`` : une boucle
    ``$source`` lit ``$.key`` et ``$.value`` par leur nom, là où un tableau
    imposerait un accès par indice, muet à la lecture.
    """
    obj = _as_object(token)
    if obj is None:
        return None
    return [{"key": key, "value": value} for key, value in obj.items()]


@jslt_function(
    "fromentries",
    description="Reconstruit un objet depuis un tableau de { key, value } ou de paires [clé, valeur]",
)
def execute_fromentries(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    if not isinstance(token, list):
        raise JsltError(f"fromentries attend un tableau d'entrées, reçu : {token!r}")
    result: dict[str, Any] = {}
    for entry in token:
        if isinstance(entry, dict) and "key" in entry:
            result[to_text(entry["key"])] = entry.get("value")
        elif isinstance(entry, list) and len(entry) == 2:
            result[to_text(entry[0])] = entry[1]
        else:
            # Ni {key, value} ni paire : on refuse plutôt que de deviner, sinon
            # une entrée mal formée disparaîtrait sans bruit du résultat.
            raise JsltError(
                "entrée invalide pour fromentries (attendu { key, value } ou "
                f"[clé, valeur]) : {entry!r}"
            )
    return result


@jslt_function(
    "merge",
    description="Fusionne deux objets, la droite gagnant les clés communes (deep à true pour fusionner les sous-objets)",
)
def execute_merge(ctx: Any, left: Any = None, right: Any = None, deep: Any = None) -> Any:
    """Fusion de deux objets, sans toucher aux sources.

    Plate par défaut : une clé commune est **remplacée**, y compris si sa valeur
    est un objet. ``deep`` descend dans les sous-objets. Le .NET mutait sa source
    dans ``join`` ; ici les deux entrées sortent intactes (copie profonde des
    valeurs reprises).
    """
    if left is None and right is None:
        return None
    for side in (left, right):
        if side is not None and not isinstance(side, dict):
            raise JsltError(f"merge attend des objets, reçu : {side!r}")
    if left is None or right is None:
        return copy.deepcopy(left if right is None else right)
    return _merge(left, right, coerce_bool(deep))


def _merge(left: dict, right: dict, deep: bool) -> dict:
    merged = copy.deepcopy(left)
    for key, value in right.items():
        if deep and isinstance(merged.get(key), dict) and isinstance(value, dict):
            merged[key] = _merge(merged[key], value, True)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def _key_list(keys: Any) -> list[str]:
    """Liste de clés acceptant un tableau ou une clé seule.

    Écrire ``pick($.o, "a")`` pour une seule clé est naturel ; l'imposer en
    tableau d'un élément serait une friction sans contrepartie.
    """
    if keys is None:
        return []
    if isinstance(keys, list):
        return [to_text(key) for key in keys]
    return [to_text(keys)]


@jslt_function("pick", description="Sous-objet limité aux clés demandées (une clé ou un tableau de clés)")
def execute_pick(ctx: Any, token: Any = None, keys: Any = None) -> Any:
    obj = _as_object(token)
    if obj is None:
        return None
    wanted = set(_key_list(keys))
    # Parcours de l'objet, pas de la liste de clés : l'ordre du document est
    # conservé, et une clé demandée mais absente est simplement absente —
    # `pick` sert justement sur des documents hétérogènes.
    return {key: value for key, value in obj.items() if key in wanted}


@jslt_function("omit", description="Objet privé des clés demandées (une clé ou un tableau de clés)")
def execute_omit(ctx: Any, token: Any = None, keys: Any = None) -> Any:
    obj = _as_object(token)
    if obj is None:
        return None
    unwanted = set(_key_list(keys))
    return {key: value for key, value in obj.items() if key not in unwanted}


@jslt_function(
    "has",
    description="Vrai si l'objet porte cette clé, même avec une valeur nulle",
)
def execute_has(ctx: Any, token: Any = None, key: Any = None) -> bool:
    """Présence d'une clé — ce qu'``isnull`` ne sait pas dire.

    ``isnull($.o.a)`` est vrai pour une clé absente **comme** pour une clé
    présente valant ``null`` ; distinguer les deux est parfois tout l'enjeu
    (champ non renseigné contre champ absent du flux).
    """
    obj = _as_object(token)
    return False if obj is None else to_text(key) in obj


@jslt_function(
    "renamekeys",
    description="Renomme les clés d'un objet selon un mapping { ancien: nouveau }",
)
def execute_renamekeys(ctx: Any, token: Any = None, mapping: Any = None) -> Any:
    obj = _as_object(token)
    if obj is None:
        return None
    table = _as_object(mapping) or {}
    renamed: dict[str, Any] = {}
    for key, value in obj.items():
        # Collision : le dernier écrit gagne, dans l'ordre du document. Lever
        # serait plus strict mais rendrait le renommage impraticable sur un flux
        # qui porte déjà les deux noms pendant une migration.
        renamed[to_text(table.get(key, key))] = value
    return renamed
