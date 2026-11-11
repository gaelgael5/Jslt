"""Structures profondes : ``flattenobject``, ``unflatten``, ``walk``, ``prune``,
``setpath``, ``unsetpath``.

Le langage savait **lire** profond (``$..k``) et **construire** plat, clé par
clé. Il ne savait pas transformer en profondeur : aplatir vers des clés pointées
(le pont vers un CSV), appliquer une règle à chaque nœud, ou poser une valeur au
bout d'un chemin sans réécrire tout l'objet autour.

Deux conventions traversent ce module :

* aucune fonction ne modifie son entrée — on rend une copie, comme ``merge`` ;
* un **conflit de chemin** lève. Écraser un scalaire pour y descendre produirait
  un document plausible où une donnée a disparu, ce qui se découvre loin de la
  cause.
"""

from __future__ import annotations

import copy
from typing import Any

from urban_json.errors import JsltError

from ._helpers import to_text
from ._lazy import evaluate_for
from .registry import jslt_function

_SEPARATOR = "."


def _separator(value: Any) -> str:
    text = _SEPARATOR if value is None else to_text(value)
    if not text:
        raise JsltError("séparateur de chemin vide : impossible de découper une clef")
    return text


# --- aplatir et reconstruire ---------------------------------------------------


@jslt_function(
    "flattenobject",
    description="Aplatit un objet en clés pointées (a.b.c), tableaux indexés par leur position",
    description_en="Flattens an object into dotted keys (a.b.c), arrays indexed by their position",
)
def execute_flattenobject(ctx: Any, token: Any = None, separator: Any = None) -> Any:
    """Objet imbriqué -> objet plat. Le pont vers un format tabulaire."""
    if not isinstance(token, (dict, list)):
        return None
    flat: dict[str, Any] = {}
    _flatten_into(token, "", _separator(separator), flat)
    return flat


def _flatten_into(value: Any, prefix: str, separator: str, flat: dict[str, Any]) -> None:
    if isinstance(value, dict) and value:
        for key, child in value.items():
            _flatten_into(child, f"{prefix}{separator}{key}" if prefix else to_text(key), separator, flat)
        return
    if isinstance(value, list) and value:
        for index, child in enumerate(value):
            _flatten_into(child, f"{prefix}{separator}{index}" if prefix else str(index), separator, flat)
        return
    # Feuille — y compris un conteneur **vide** : sans cela une clé valant {}
    # disparaîtrait, et l'aller-retour perdrait de l'information.
    flat[prefix] = value


@jslt_function(
    "unflatten",
    description="Reconstruit un objet imbriqué depuis des clés pointées (arrays à true pour les indices)",
    description_en="Rebuilds a nested object from dotted keys (arrays true for the indices)",
)
def execute_unflatten(
    ctx: Any, token: Any = None, separator: Any = None, arrays: Any = None
) -> Any:
    """Inverse de ``flattenobject``.

    Les segments numériques ne redeviennent des **tableaux** que si on le
    demande : une clé « 2026 » est un nom d'année dans bien des documents, et en
    faire un indice créerait un tableau de deux mille trous.
    """
    if not isinstance(token, dict):
        return None
    sep = _separator(separator)
    nested: dict[str, Any] = {}
    for key, value in token.items():
        _place(nested, to_text(key).split(sep), value, key)
    return _indexed(nested) if arrays is True else nested


def _place(target: dict[str, Any], steps: list[str], value: Any, origin: Any) -> None:
    for position, step in enumerate(steps[:-1]):
        child = target.get(step)
        if child is None:
            child = target[step] = {}
        elif not isinstance(child, dict):
            raise JsltError(
                f"conflit de chemin à {separator_join(steps[: position + 1])!r} "
                f"(clef {origin!r}) : une valeur occupe déjà ce niveau"
            )
        target = child
    if isinstance(target.get(steps[-1]), dict) and target[steps[-1]]:
        raise JsltError(f"conflit de chemin pour la clef {origin!r} : un objet occupe déjà ce nom")
    target[steps[-1]] = value


def separator_join(steps: list[str]) -> str:
    return _SEPARATOR.join(steps)


def _indexed(value: Any) -> Any:
    """Convertit en tableau tout objet dont les clés sont 0..n-1."""
    if not isinstance(value, dict):
        return value
    converted = {key: _indexed(child) for key, child in value.items()}
    if converted and all(key.isdigit() for key in converted):
        order = sorted(converted, key=int)
        if [int(key) for key in order] == list(range(len(order))):
            return [converted[key] for key in order]
    return converted


# --- parcourir et nettoyer -----------------------------------------------------


@jslt_function(
    "walk",
    lazy_args=(1,),
    description="Applique une expression à chaque nœud d'une structure, des feuilles vers la racine",
    description_en="Applies an expression to every node of a structure, from the leaves to the root",
)
def execute_walk(ctx: Any, token: Any = None, expression: Any = None) -> Any:
    """Transformation récursive, **des feuilles vers la racine**.

    Dans ce sens, l'expression voit des enfants déjà transformés, donc une règle
    qui dépend de ses enfants (« retirer les objets devenus vides ») fonctionne.
    Dans l'autre sens, elle verrait l'original et devrait redescendre elle-même.
    """
    if expression is None:
        return token
    return _walk(ctx, token, expression)


def _walk(ctx: Any, value: Any, expression: Any) -> Any:
    if isinstance(value, dict):
        value = {key: _walk(ctx, child, expression) for key, child in value.items()}
    elif isinstance(value, list):
        value = [_walk(ctx, child, expression) for child in value]
    return evaluate_for(ctx, value, expression)


_PRUNE_OPTIONS = ("null", "empty")


@jslt_function(
    "prune",
    description="Retire récursivement les null d'une structure, et le vide avec l'option empty",
    description_en="Recursively removes the nulls of a structure, and the empties with the empty option",
)
def execute_prune(ctx: Any, token: Any = None, options: Any = None) -> Any:
    """Nettoyage d'un document creux.

    ``null`` seul par défaut : une chaîne vide, un tableau vide et ``0`` sont des
    **valeurs**, et les retirer d'office ferait disparaître un « montant : 0 »
    qui dit quelque chose. L'option ``empty`` est là pour qui veut l'inverse.
    """
    name = "null" if options is None else to_text(options).strip().lower()
    if name not in _PRUNE_OPTIONS:
        raise JsltError(
            f"option de prune inconnue : {options!r} (attendu : {', '.join(_PRUNE_OPTIONS)})"
        )
    return _prune(token, name == "empty")


def _prune(value: Any, drop_empty: bool) -> Any:
    if isinstance(value, dict):
        kept = {}
        for key, child in value.items():
            pruned = _prune(child, drop_empty)
            if not _droppable(pruned, drop_empty):
                kept[key] = pruned
        return kept
    if isinstance(value, list):
        return [
            pruned
            for pruned in (_prune(child, drop_empty) for child in value)
            if not _droppable(pruned, drop_empty)
        ]
    return value


def _droppable(value: Any, drop_empty: bool) -> bool:
    if value is None:
        return True
    # `0` et `false` ne sont pas vides : ce sont des valeurs. D'où le test de
    # longueur plutôt que la véracité.
    return drop_empty and isinstance(value, (str, list, dict)) and len(value) == 0


# --- poser et retirer une valeur -----------------------------------------------


@jslt_function(
    "setpath",
    description="Copie de l'objet avec une valeur posée au bout d'un chemin pointé (niveaux créés au besoin)",
    description_en="Copy of the object with a value placed at the end of a dotted path (levels created as needed)",
)
def execute_setpath(
    ctx: Any, token: Any = None, path: Any = None, value: Any = None, separator: Any = None
) -> Any:
    if not isinstance(token, (dict, list)):
        return None
    steps = to_text(path).split(_separator(separator))
    result = copy.deepcopy(token)
    _assign(result, steps, value)
    return result


def _assign(target: Any, steps: list[str], value: Any) -> None:
    for position, step in enumerate(steps[:-1]):
        child = _child(target, step)
        if child is None or not isinstance(child, (dict, list)):
            if child is not None:
                raise JsltError(
                    f"conflit de chemin à {separator_join(steps[: position + 1])!r} : "
                    f"une valeur ({child!r}) occupe déjà ce niveau"
                )
            child = {}
            _set_child(target, step, child)
        target = child
    _set_child(target, steps[-1], value)


def _child(target: Any, step: str) -> Any:
    if isinstance(target, list):
        index = _index(target, step)
        return target[index] if index is not None else None
    return target.get(step)


def _set_child(target: Any, step: str, value: Any) -> None:
    if isinstance(target, list):
        index = _index(target, step)
        if index is None:
            raise JsltError(f"indice hors bornes ou non numérique dans un tableau : {step!r}")
        target[index] = value
        return
    target[step] = value


def _index(target: list, step: str) -> int | None:
    if not step.lstrip("-").isdigit():
        return None
    index = int(step)
    return index if -len(target) <= index < len(target) else None


@jslt_function(
    "unsetpath",
    description="Copie de l'objet privée du chemin pointé (sans erreur s'il est absent)",
    description_en="Copy of the object without the dotted path (no error when it is absent)",
)
def execute_unsetpath(
    ctx: Any, token: Any = None, path: Any = None, separator: Any = None
) -> Any:
    """Retire un chemin. Un chemin absent n'est **pas** une erreur : on demande
    un document sans cette donnée, et il l'est déjà."""
    if not isinstance(token, (dict, list)):
        return None
    steps = to_text(path).split(_separator(separator))
    result = copy.deepcopy(token)
    target = result
    for step in steps[:-1]:
        target = _child(target, step)
        if not isinstance(target, (dict, list)):
            return result
    last = steps[-1]
    if isinstance(target, list):
        index = _index(target, last)
        if index is not None:
            del target[index]
    elif isinstance(target, dict):
        target.pop(last, None)
    return result
