"""Fonctions de collection (port des ``Services.distinct`` / ``Services.group``,
étendu).

``select`` et ``selectmany`` reçoivent leur chemin comme argument compilé
(``path_args``), appliqué au document source.

Au-delà du .NET : ``skip``, ``flatten``, ``zip``, ``unzip``, ``chunk``, ``window``,
``partition``, ``distinctby``, ``intersect``, ``difference``. Les deux dernières
comparent la **structure** (clef d'ordre de :mod:`.ordering`) et non l'égalité
``==`` du langage — voir ``_set_operation``.
"""

from __future__ import annotations

from typing import Any

from urban_json.errors import JsltError

from ._helpers import as_json_path, coerce_bool, coerce_number
from ._lazy import evaluate_for
from .ordering import order_key
from .registry import jslt_function


@jslt_function("limit", description="Les max_items premiers éléments d'un tableau", description_en="The first max_items elements of an array")
def execute_limit(ctx: Any, source: Any = None, max_items: int = 0) -> Any:
    """Les ``max_items`` premiers éléments d'un tableau (port de ``ExecuteLimit``)."""
    if isinstance(source, list):
        return source[:max_items]
    return None


@jslt_function("union", description="Aplatit d'un niveau un tableau de tableaux", description_en="Flattens an array of arrays by one level")
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


@jslt_function("select", path_args=(1,), description="Première valeur sélectionnée par un chemin JSONPath dans la source, ou null", description_en="First value selected by a JSONPath path in the source, or null")
def execute_select(ctx: Any, source: Any = None, path: Any = None) -> Any:
    """Première valeur sélectionnée par le chemin (port de ``ExecuteSelectOne``)."""
    path = as_json_path(path)
    if source is None or path is None:
        return None
    values = path.select_values(source)
    return values[0] if values else None


@jslt_function("selectmany", path_args=(1,), description="Toutes les valeurs sélectionnées par un chemin JSONPath dans la source", description_en="All the values selected by a JSONPath path in the source")
def execute_selectmany(ctx: Any, source: Any = None, path: Any = None) -> list:
    """Toutes les valeurs sélectionnées par le chemin (port de ``ExecuteSelectMany``)."""
    path = as_json_path(path)
    if source is None or path is None:
        return []
    return path.select_values(source)


@jslt_function("any", description="Vrai si la source est un tableau non vide (avec un prédicat, c'est some)", description_en="True when the source is a non-empty array (with a predicate, that is some)")
def execute_any(ctx: Any, source: Any = None) -> bool:
    # Port de ExecuteAny : seul un tableau compte, un objet ou une chaîne donnent faux.
    return isinstance(source, list) and len(source) > 0


@jslt_function("contains", description="Vrai si le tableau contient un élément égal à la valeur", description_en="True when the array holds an element equal to the value")
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
    description_en="True when the JSONPath path selects at least one value in the source",
)
def execute_selectany(ctx: Any, source: Any = None, path: Any = None) -> bool:
    path = as_json_path(path)
    if source is None or path is None:
        return False
    # Nœuds sélectionnés, pas valeurs vraies : une valeur 0 ou "" trouvée compte.
    return len(path.evaluate(source)) > 0


# --- Parcours et découpage -----------------------------------------------------
# Sans contrepartie .NET. Convention de la famille, celle de `limit` : `null` et
# une valeur qui n'est pas un tableau donnent `null` — rendre `[]` ferait passer
# une erreur de chemin pour une collection vide.


@jslt_function("skip", description="Ignore les n premiers éléments d'un tableau (complément de limit)", description_en="Drops the first n elements of an array (the complement of limit)")
def execute_skip(ctx: Any, source: Any = None, count: Any = 0) -> Any:
    """Complément de ``limit`` : sans lui, pas de pagination."""
    if not isinstance(source, list):
        return None
    start = max(int(coerce_number(count)), 0)  # un saut négatif ne saute rien
    return source[start:]


@jslt_function(
    "flatten",
    description="Aplatit un tableau de tableaux, à fond par défaut ou sur depth niveaux",
    description_en="Flattens an array of arrays, all the way down by default or over depth levels",
)
def execute_flatten(ctx: Any, source: Any = None, depth: Any = None) -> Any:
    """Aplatissement **récursif**, là où ``union`` ne descend que d'un niveau."""
    if not isinstance(source, list):
        return None
    if depth is None:
        levels = -1  # jusqu'au bout
    else:
        levels = int(coerce_number(depth))
        if levels < 0:
            raise JsltError(f"profondeur négative interdite pour flatten : {depth!r}")
    return _flatten(source, levels)


def _flatten(source: list, levels: int) -> list:
    result: list = []
    for item in source:
        if isinstance(item, list) and levels != 0:
            result.extend(_flatten(item, levels - 1))
        else:
            result.append(item)
    return result


@jslt_function("zip", description="Apparie deux tableaux élément par élément, en s'arrêtant au plus court", description_en="Pairs two arrays element by element, stopping at the shorter one")
def execute_zip(ctx: Any, left: Any = None, right: Any = None) -> Any:
    if not isinstance(left, list) or not isinstance(right, list):
        return None
    # Troncature au plus court plutôt que remplissage par `null` : un appariement
    # inventé serait indiscernable d'une vraie valeur nulle.
    return [[a, b] for a, b in zip(left, right)]


@jslt_function(
    "unzip",
    description="Inverse de zip : d'un tableau de rangées, rend un tableau par position",
    description_en="Converse of zip: from an array of rows, returns one array per position",
)
def execute_unzip(ctx: Any, source: Any = None) -> Any:
    """Réciproque de ``zip`` : sans elle, un appariement ne se défaisait pas."""
    if not isinstance(source, list):
        return None
    for row in source:
        if not isinstance(row, list):
            # Écart assumé à la convention de la famille (non-tableau -> null) :
            # ici la source *est* un tableau, donc le chemin était bon ; c'est la
            # donnée qui n'a pas la forme attendue, et un `null` global ferait
            # chercher l'erreur dans le chemin.
            raise JsltError(f"unzip attend un tableau de tableaux, reçu : {row!r}")
    if not source:
        return []
    # Troncature à la rangée la plus courte, symétrique de `zip` qui s'arrête au
    # plus court : compléter par `null` inventerait des valeurs indiscernables
    # des vraies.
    width = min(len(row) for row in source)
    return [[row[index] for row in source] for index in range(width)]


@jslt_function("chunk", description="Découpe un tableau en tranches consécutives de size éléments", description_en="Cuts an array into consecutive slices of size elements")
def execute_chunk(ctx: Any, source: Any = None, size: Any = 0) -> Any:
    width = _width(size, "chunk")
    if not isinstance(source, list):
        return None
    return [source[start : start + width] for start in range(0, len(source), width)]


@jslt_function(
    "window",
    description="Fenêtres glissantes de size éléments consécutifs (vide si le tableau est plus court)",
    description_en="Sliding windows of size consecutive elements (empty when the array is shorter)",
)
def execute_window(ctx: Any, source: Any = None, size: Any = 0) -> Any:
    width = _width(size, "window")
    if not isinstance(source, list):
        return None
    return [source[start : start + width] for start in range(len(source) - width + 1)]


def _width(size: Any, name: str) -> int:
    width = int(coerce_number(size))
    if width <= 0:
        # Une tranche de taille nulle boucle à l'infini : c'est une faute
        # d'écriture du template, pas une donnée surprenante.
        raise JsltError(f"taille de tranche invalide pour {name} : {size!r} (attendu : > 0)")
    return width


@jslt_function(
    "partition",
    lazy_args=(1,),
    description="Sépare un tableau en { true, false } selon un prédicat évalué par élément",
    description_en="Splits an array into { true, false } according to a predicate evaluated per element",
)
def execute_partition(ctx: Any, source: Any = None, predicate: Any = None) -> Any:
    """Les deux côtés d'un filtre, en une passe.

    Un objet à deux clés plutôt que deux appels de filtre : on parcourt une
    fois, et le lecteur voit que les deux ensembles sont complémentaires.
    """
    if not isinstance(source, list):
        return None
    kept: list = []
    dropped: list = []
    for item in source:
        (kept if coerce_bool(evaluate_for(ctx, item, predicate)) else dropped).append(item)
    return {"true": kept, "false": dropped}


@jslt_function(
    "distinctby",
    lazy_args=(1,),
    description="Déduplique un tableau sur une clef calculée par élément, en gardant le premier",
    description_en="Deduplicates an array on a key computed per element, keeping the first",
)
def execute_distinctby(ctx: Any, source: Any = None, key: Any = None) -> Any:
    """Déduplication d'**objets**, que ``distinct`` ne sait pas faire (il ignore
    les objets et travaille sur les valeurs sélectionnées par un chemin)."""
    if not isinstance(source, list):
        return None
    seen: set = set()
    result: list = []
    for item in source:
        marker = order_key(evaluate_for(ctx, item, key))
        if marker not in seen:
            seen.add(marker)
            result.append(item)
    return result


@jslt_function("intersect", description="Éléments du tableau de gauche présents aussi à droite, dédupliqués", description_en="Elements of the left array also present on the right, deduplicated")
def execute_intersect(ctx: Any, left: Any = None, right: Any = None) -> Any:
    return _set_operation(left, right, keep=True)


@jslt_function("difference", description="Éléments du tableau de gauche absents du tableau de droite, dédupliqués", description_en="Elements of the left array absent from the right one, deduplicated")
def execute_difference(ctx: Any, left: Any = None, right: Any = None) -> Any:
    return _set_operation(left, right, keep=False)


def _set_operation(left: Any, right: Any, keep: bool) -> Any:
    """Opération ensembliste, ordre de gauche conservé, doublons retirés.

    Égalité **structurelle** (la clef d'ordre), et non l'égalité ``==`` du
    langage où ``"2" == 2`` : sur un ensemble, confondre les deux rendrait le
    résultat imprévisible selon l'ordre des éléments.
    """
    if not isinstance(left, list) or not isinstance(right, list):
        return None
    other = {order_key(item) for item in right}
    seen: set = set()
    result: list = []
    for item in left:
        marker = order_key(item)
        if (marker in other) == keep and marker not in seen:
            seen.add(marker)
            result.append(item)
    return result
