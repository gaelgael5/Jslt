"""Agrégation par clef calculée : ``groupby``, ``countby``, ``sumby``, ``avgby``.

Famille extraite de :mod:`.aggregate`, qui garde les statistiques : les quatre
fonctions partagent la même clef (une expression évaluée **par élément**, cf.
:mod:`._lazy`) et la même mise en texte de cette clef, et une divergence entre
elles sur ce point serait invisible au lecteur.

``group`` (:mod:`.grouping`) reste la forme .NET (``Label`` / ``Items``) ; ici
le regroupement rend un **objet**, donc réductible par ``entries``.
"""

from __future__ import annotations

from typing import Any

from urban_json.errors import JsltError

from ._helpers import coerce_bool, is_number, to_text
from ._lazy import evaluate_for
from .registry import jslt_function


def _label(value: Any) -> str:
    """Clef de groupe en texte : une clé d'objet JSON est une chaîne.

    Une clef composite (``[$.pays, $.ville]``) donne donc son JSON compact
    (``["FR","Lyon"]``), lisible et re-analysable — c'est la forme plate. Pour
    l'interroger par chemin, c'est ``groupby(…, true)`` qui imbrique.
    """
    return to_text(value)


@jslt_function(
    "groupby",
    lazy_args=(1,),
    description=(
        "Regroupe un tableau en un objet { clef: éléments }, clef calculée par élément ; "
        "nested imbrique un niveau par clef d'un tableau de clefs"
    ),
    description_en="Groups an array into an object { key: elements }, key computed per element; nested adds one level per key of an array of keys",
)
def execute_groupby(ctx: Any, source: Any = None, key: Any = None, nested: Any = None) -> Any:
    """Regroupement en **objet**, à plat ou imbriqué."""
    if not isinstance(source, list):
        return None
    if coerce_bool(nested):
        return _nested_groups(ctx, source, key)
    groups: dict[str, list] = {}
    for item in source:
        groups.setdefault(_label(evaluate_for(ctx, item, key)), []).append(item)
    return groups


def _nested_groups(ctx: Any, source: list, key: Any) -> dict:
    """Un niveau d'objet par composante de la clef.

    ``groupby($.l, [$.pays, $.ville], true)`` rend ``{pays: {ville: [...]}}``, que
    l'on interroge par chemin (``…FR.Lyon``) ; la forme plate rend la clef
    textuelle ``["FR","Lyon"]``, qu'il faut re-analyser pour s'en servir.
    """
    root: dict[str, Any] = {}
    for item in source:
        parts = evaluate_for(ctx, item, key)
        if not isinstance(parts, list) or not parts:
            raise JsltError(
                f"groupby imbriqué attend un tableau de clefs non vide, reçu : {parts!r}"
            )
        node = root
        for part in parts[:-1]:
            node = node.setdefault(_label(part), {})
            if not isinstance(node, dict):
                # Deux éléments dont les clefs n'ont pas la même longueur : la
                # même clef porterait à la fois des éléments et un sous-groupe.
                # Écraser l'un des deux ferait disparaître des données.
                raise JsltError(
                    "groupby imbriqué : profondeur de clef incohérente entre les éléments"
                )
        branch = node.setdefault(_label(parts[-1]), [])
        if not isinstance(branch, list):
            raise JsltError(
                "groupby imbriqué : profondeur de clef incohérente entre les éléments"
            )
        branch.append(item)
    return root


@jslt_function(
    "countby",
    lazy_args=(1,),
    description="Compte les éléments d'un tableau par clef calculée, en un objet { clef: nombre }",
    description_en="Counts the elements of an array per computed key, as an object { key: count }",
)
def execute_countby(ctx: Any, source: Any = None, key: Any = None) -> Any:
    if not isinstance(source, list):
        return None
    counts: dict[str, int] = {}
    for item in source:
        marker = _label(evaluate_for(ctx, item, key))
        counts[marker] = counts.get(marker, 0) + 1
    return counts


def _values_by_group(ctx: Any, source: Any, key: Any, value: Any, name: str) -> dict[str, list] | None:
    """Valeurs numériques d'un tableau, rangées par clef de groupe.

    Sans expression de valeur, c'est l'élément lui-même qui est agrégé (même
    convention que ``sort`` ou ``distinctby`` : l'argument paresseux omis vaut
    l'élément), ce qui permet d'agréger un tableau de nombres par une clef
    calculée.
    """
    if not isinstance(source, list):
        return None
    groups: dict[str, list] = {}
    for item in source:
        label = _label(evaluate_for(ctx, item, key))
        number = evaluate_for(ctx, item, value)
        if not is_number(number):
            # Même refus que `sum` : sauter l'intrus rendrait un total plausible
            # et faux, découvert très loin de sa cause.
            raise JsltError(f"{name} attend un nombre par élément, reçu : {number!r}")
        groups.setdefault(label, []).append(number)
    return groups


@jslt_function(
    "sumby",
    lazy_args=(1, 2),
    description="Somme par clef calculée, en un objet { clef: somme } (la valeur par défaut est l'élément)",
    description_en="Sum per computed key, as an object { key: sum } (the value defaults to the element)",
)
def execute_sumby(ctx: Any, source: Any = None, key: Any = None, value: Any = None) -> Any:
    """Le cas le plus fréquent de l'agrégation par groupe, en un appel.

    Il s'écrivait ``fromentries([{ "$source": entries(groupby(…)), … sum(selectmany(…)) }])``
    — quatre fonctions et une boucle pour un total par clef.
    """
    groups = _values_by_group(ctx, source, key, value, "sumby")
    if groups is None:
        return None
    return {label: sum(values) for label, values in groups.items()}


@jslt_function(
    "avgby",
    lazy_args=(1, 2),
    description="Moyenne par clef calculée, en un objet { clef: moyenne } (la valeur par défaut est l'élément)",
    description_en="Mean per computed key, as an object { key: mean } (the value defaults to the element)",
)
def execute_avgby(ctx: Any, source: Any = None, key: Any = None, value: Any = None) -> Any:
    groups = _values_by_group(ctx, source, key, value, "avgby")
    if groups is None:
        return None
    # Pas de groupe vide possible (un groupe naît d'un élément), donc pas de
    # division par zéro à couvrir ici — contrairement à `avg([])`, qui rend null.
    return {label: sum(values) / len(values) for label, values in groups.items()}
