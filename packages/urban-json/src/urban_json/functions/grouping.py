"""Regroupement et jointure : group, join, createindex, index.

Port de ``Services.group.cs`` (.NET). Les clés sont comparées en texte, comme le
.NET (``Value.ToString()``) : ``10`` et ``"10"`` désignent la même clé.

Écarts volontaires (comportement voulu, pas les bugs) :

* ``group`` sur plusieurs chemins : le .NET perdait les sous-groupes
  (``GroupIndex.Collect`` ne les ajoutait que si le niveau portait des éléments
  directs, ce qui n'arrive qu'au dernier niveau) ; ici chaque niveau contient
  ses sous-groupes ``{Label, Items}``.
* ``join`` travaille sur une copie : le .NET modifiait les objets de la source
  gauche, donc tout ``$.x`` relu ensuite dans le template.
* ``createindex`` rend un objet JSON ``{clé: élément}`` (le .NET rendait un
  ``JDictionaryValue`` opaque) : ``index(i, clé)`` y lit, et il reste lisible
  s'il est émis tel quel.
"""

from __future__ import annotations

import copy
from typing import Any

from urban_json.errors import JsltError

from ._helpers import as_json_path, to_text
from .registry import jslt_function


def _first(path: Any, item: Any) -> Any:
    values = path.select_values(item)
    return values[0] if values else None


def _key(path: Any, item: Any) -> str | None:
    """Clé texte d'un élément (``None`` si absente ou non scalaire)."""
    value = _first(path, item)
    if value is None or isinstance(value, (dict, list)):
        return None
    return to_text(value)


def _group_level(items: list, paths: list) -> list[dict]:
    groups: dict[str, list] = {}
    for item in items:
        key = _key(paths[0], item)
        if key is not None:
            groups.setdefault(key, []).append(item)
    rest = paths[1:]
    return [
        {"Label": label, "Items": _group_level(members, rest) if rest else members}
        for label, members in groups.items()
    ]


@jslt_function(
    "group",
    description="Regroupe un tableau par chemins JSONPath successifs en {Label, Items} imbriqués",
)
def execute_group(ctx: Any, source: Any = None, group_paths: Any = None) -> list:
    if not isinstance(source, list) or not group_paths:
        return []
    if not isinstance(group_paths, list):
        group_paths = [group_paths]
    paths = [as_json_path(p) for p in group_paths if p is not None]
    return _group_level(source, paths) if paths else []


def _right_rule(rule: Any) -> tuple[str, Any, list]:
    if not isinstance(rule, dict) or not rule.get("Name") or not rule.get("Key"):
        raise JsltError(
            f"join : règle de droite invalide {rule!r} — attendu {{ \"Name\": …, \"Key\": \"$.chemin\", \"Source\": [...] }}"
        )
    source = rule.get("Source")
    return to_text(rule["Name"]), as_json_path(rule["Key"]), source if isinstance(source, list) else []


@jslt_function(
    "join",
    path_args=(1,),
    description="Jointure gauche : rattache aux objets de gauche les éléments de droite de même clé",
)
def execute_join(
    ctx: Any, source_left: Any = None, key_left: Any = None, clean_source: Any = None, rights: Any = None
) -> Any:
    # clean_source libérait la mémoire côté .NET (GC) : sans objet ici, accepté et ignoré.
    if not isinstance(source_left, list):
        return None
    key_path = as_json_path(key_left)
    rules = [_right_rule(rule) for rule in (rights or [])]
    left = copy.deepcopy(source_left)
    for name, right_key, right_source in rules:
        by_key: dict[str, list] = {}
        for item in right_source:
            key = _key(right_key, item)
            if key is not None:
                by_key.setdefault(key, []).append(item)
        for item in left:
            if not isinstance(item, dict):
                continue
            matches = by_key.get(_key(key_path, item) or "", [])
            if matches:
                item[name] = [_without_key(match, right_key) for match in matches]
    return left


def _without_key(item: Any, key_path: Any) -> Any:
    """Copie de l'élément de droite sans sa propriété de clé (comme le .NET)."""
    clone = copy.deepcopy(item)
    for node in key_path.evaluate(clone):
        if not node.location:
            continue
        parent: Any = clone
        for step in node.location[:-1]:
            parent = parent[step]
        name = node.location[-1]
        if isinstance(parent, dict) and name in parent:
            del parent[name]
    return clone


@jslt_function(
    "createindex",
    description="Construit un index {clé: élément} à partir d'une source, d'un chemin de découpe et d'un chemin de clé",
)
def execute_createindex(ctx: Any, source: Any = None, object_path: Any = None, key: Any = None) -> dict:
    index: dict[str, Any] = {}
    if source is None or source == [] or source == {}:
        return index
    split = as_json_path(object_path) if object_path not in (None, "") else None
    items = split.select_values(source) if split is not None else (source if isinstance(source, list) else [source])
    key_path = as_json_path(key)
    if key_path is None:
        return index
    for item in items:
        value = _key(key_path, item)
        if value is not None and value not in index:  # doublon : le 1er gagne (comme le .NET)
            index[value] = item
    return index


@jslt_function("index", description="Élément d'un index (créé par createindex) pour une clé, ou null")
def execute_index(ctx: Any, index: Any = None, key: Any = None) -> Any:
    if not isinstance(index, dict) or key is None:
        return None
    return index.get(to_text(key))
