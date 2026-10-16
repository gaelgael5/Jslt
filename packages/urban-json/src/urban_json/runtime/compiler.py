"""Compilation de l'AST en closures (chemin d'exécution rapide).

Le .NET générait puis compilait du code (Roslyn). Le portage garde un
interpréteur d'AST (tree-walking) comme chemin par défaut — simple et portable —
et ajoute **ici** un chemin *compilé* optionnel pour les transformations en
masse (gros volumes).

Principe : parcourir l'AST **une seule fois** et produire, par nœud, une closure
``program(context) -> valeur`` qui capture les closures de ses enfants. À
l'exécution, il n'y a plus de double-dispatch ``accept``/``visit_*`` ni de tests
de type répétés — seulement des appels de closures composées. La sémantique est
**strictement celle de** :class:`urban_json.runtime.evaluator.JsltEvaluationVisitor`
(mêmes helpers, même ordre d'évaluation) ; les deux chemins doivent produire des
résultats identiques (vérifié par les tests).

Tout type de nœud non explicitement compilé retombe sur l'interpréteur (closure
de repli) : le chemin compilé est donc toujours correct, jamais plus faux que
l'interpréteur.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from urban_json.ast import (
    JsltArray,
    JsltBinaryOperator,
    JsltConstant,
    JsltFunctionCall,
    JsltObject,
    JsltOperator,
    JsltPath,
    JsltSwitch,
    JsltVariable,
    OperationEnum,
)
from urban_json.errors import JsltError
from urban_json.jsonpath.selectors import NameSelector

from .operators import apply_unary, binary_op

if TYPE_CHECKING:
    from urban_json.ast import JsltBase

    from .context import RuntimeContext

#: Une closure compilée : prend le contexte d'exécution et renvoie la valeur JSON.
Program = Callable[["RuntimeContext"], Any]


def _none(ctx: RuntimeContext) -> None:
    return None


def compile_program(node: JsltBase) -> Program:
    """Compile un AST en une closure ``program(context) -> valeur``."""
    return _compile(node)


def _compile(node: JsltBase) -> Program:
    compiler = _DISPATCH.get(type(node))
    if compiler is not None:
        return compiler(node)
    return _compile_fallback(node)


# --- feuilles --------------------------------------------------------------

def _c_constant(node: JsltConstant) -> Program:
    value = node.value
    return lambda ctx: value


def _singular_steps(compiled) -> list[tuple[bool, Any]]:
    """(is_name, key) par segment d'un chemin singulier : nom de dict ou indice."""
    return [
        (isinstance(seg.selectors[0], NameSelector),
         seg.selectors[0].name if isinstance(seg.selectors[0], NameSelector)
         else seg.selectors[0].index)
        for seg in compiled.segments
    ]


def _descend(source: Any, steps: list[tuple[bool, Any]]) -> Any:
    """Descente directe d'un chemin singulier (noms/indices), ``None`` si absent.

    Reproduit ``select_values`` d'un chemin ``is_singular`` sans allouer de
    ``Node`` ni passer par le moteur générique : mêmes règles que
    ``NameSelector``/``IndexSelector`` (nom absent, non-dict, indice hors bornes,
    non-list → aucune correspondance → ``None``).
    """
    cur = source
    for is_name, key in steps:
        if is_name:
            if not isinstance(cur, dict) or key not in cur:
                return None
            cur = cur[key]
        else:
            if not isinstance(cur, list):
                return None
            count = len(cur)
            index = key + count if key < 0 else key
            if not (0 <= index < count):
                return None
            cur = cur[index]
    return cur


def _c_path(node: JsltPath) -> Program:
    compiled = node.compiled
    variable = node.variable

    # Chemin singulier (noms/indices) : accès direct, sans moteur générique.
    if compiled.is_singular:
        steps = _singular_steps(compiled)
        # Cas ultra-courant `$.champ` (un seul nom, source courante) : accès direct.
        if variable is None and len(steps) == 1 and steps[0][0]:
            key = steps[0][1]

            def prog(ctx: RuntimeContext) -> Any:
                src = ctx.current_source
                return src.get(key) if isinstance(src, dict) else None

            return prog
        if variable is None:
            return lambda ctx: _descend(ctx.current_source, steps)
        return lambda ctx: _descend(ctx.variables.get(variable)[1], steps)

    # Chemin général (wildcard, descente, slices, filtres) : moteur complet.
    if variable is not None:
        def prog(ctx: RuntimeContext) -> Any:
            _, root = ctx.variables.get(variable)
            values = compiled.select_values(root)
            if not values:
                return None
            if len(values) == 1:
                return values[0]
            return values
    else:
        def prog(ctx: RuntimeContext) -> Any:
            values = compiled.select_values(ctx.current_source)
            if not values:
                return None
            if len(values) == 1:
                return values[0]
            return values
    return prog


def _c_variable(node: JsltVariable) -> Program:
    name = node.name
    return lambda ctx: ctx.variables.get(name)[1]


# --- opérateurs ------------------------------------------------------------

def _c_binary(node: JsltBinaryOperator) -> Program:
    op = node.operator
    cleft = _compile(node.left)

    if op is OperationEnum.COALESCE:
        cright = _compile(node.right)

        def prog(ctx: RuntimeContext) -> Any:
            left = cleft(ctx)
            return left if left is not None else cright(ctx)

        return prog

    if op is OperationEnum.CHAIN:
        def prog(ctx: RuntimeContext) -> Any:
            raise NotImplementedError("opérateur de chaînage '->' : Phase 4")

        return prog

    cright = _compile(node.right)
    operation = binary_op(op)  # opérateur pré-résolu (pas de ré-aiguillage)

    def prog(ctx: RuntimeContext) -> Any:
        return operation(cleft(ctx), cright(ctx))

    return prog


def _c_unary(node: JsltOperator) -> Program:
    op = node.operator
    cleft = _compile(node.left)
    return lambda ctx: apply_unary(op, cleft(ctx))


# --- fonctions & switch ----------------------------------------------------

def _c_function(node: JsltFunctionCall) -> Program:
    name = node.name
    args = node.arguments
    compiled_args = [_compile(a) for a in args]
    is_path = [isinstance(a, JsltPath) for a in args]
    path_objs = [a.compiled if isinstance(a, JsltPath) else None for a in args]
    count = len(args)

    def prog(ctx: RuntimeContext) -> Any:
        function = ctx.functions.get(name)
        if function is None:
            raise JsltError(f"fonction inconnue : {name}")
        path_args = ctx.functions.path_args_of(name)
        values = []
        for index in range(count):
            if is_path[index] and index in path_args:
                values.append(path_objs[index])
            else:
                values.append(compiled_args[index](ctx))
        return function(ctx, *values)

    return prog


def _c_switch(node: JsltSwitch) -> Program:
    cexpr = _compile(node.expression)
    cases = [
        (_compile(case.right_expression),
         _compile(case.block) if case.block is not None else _none)
        for case in node.cases
    ]
    cdefault = _compile(node.default) if node.default is not None else None
    equal = binary_op(OperationEnum.EQUAL)

    def prog(ctx: RuntimeContext) -> Any:
        left = cexpr(ctx)
        for cright, cblock in cases:
            if equal(left, cright(ctx)) is True:
                return cblock(ctx)
        return cdefault(ctx) if cdefault is not None else None

    return prog


# --- objets & tableaux -----------------------------------------------------

def _compile_object_body(node: JsltObject) -> Program:
    """Compile le corps d'un objet (variables + propriétés), sans ``$source``.

    Les variables sont évaluées hâtivement dans un scope propre à l'objet
    (chaîné au parent), avant les propriétés — exactement comme
    ``JsltEvaluationVisitor._evaluate_object_body``.
    """
    cvars = [
        (v.name, _compile(v.value) if v.value is not None else _none)
        for v in node.variables
    ]
    cprops = [
        (p.name, _compile(p.value) if p.value is not None else _none)
        for p in node.properties
    ]
    # Cas courant sans variable : pas de scope à empiler ni de try/finally —
    # construction directe par compréhension.
    if not cvars:
        def body_no_vars(ctx: RuntimeContext) -> dict[str, Any]:
            return {name: cvalue(ctx) for name, cvalue in cprops}

        return body_no_vars

    def body(ctx: RuntimeContext) -> dict[str, Any]:
        previous = ctx.push_scope()
        for name, cvalue in cvars:
            ctx.variables.add(name, cvalue(ctx))
        try:
            return {name: cvalue(ctx) for name, cvalue in cprops}
        finally:
            ctx.restore_scope(previous)

    return body


def _c_object(node: JsltObject) -> Program:
    body = _compile_object_body(node)
    if node.source is None:
        return body

    csource = _compile(node.source)

    def prog(ctx: RuntimeContext) -> dict[str, Any]:
        ctx.push_source(csource(ctx))
        try:
            return body(ctx)
        finally:
            ctx.pop_source()

    return prog


def _c_array(node: JsltArray) -> Program:
    # Pré-compile chaque item : boucle ($source) ou item simple, avec son $where.
    items: list[tuple[bool, Program | None, Program | None, Program]] = []
    for item in node.items:
        cwhere = _compile(item.where) if item.where is not None else None
        if item.source is not None:
            csource = _compile(item.source)
            # Item de boucle : la source de l'élément courant est déjà empilée,
            # on construit le corps directement (sans ré-appliquer le $source).
            cbody = _compile_object_body(item) if isinstance(item, JsltObject) else _compile(item)
            items.append((True, csource, cwhere, cbody))
        else:
            items.append((False, None, cwhere, _compile(item)))

    def prog(ctx: RuntimeContext) -> list[Any]:
        result: list[Any] = []
        for is_loop, csource, cwhere, cbody in items:
            if is_loop:
                source_value = csource(ctx)
                if isinstance(source_value, list):
                    elements = source_value
                elif source_value is None:
                    elements = []
                else:
                    # Lenient vs .NET : une source unique = une itération.
                    elements = [source_value]
                for element in elements:
                    ctx.push_source(element)
                    try:
                        if cwhere is None or cwhere(ctx) is True:
                            result.append(cbody(ctx))
                    finally:
                        ctx.pop_source()
            elif cwhere is None or cwhere(ctx) is True:
                result.append(cbody(ctx))
        return result

    return prog


# --- repli (interpréteur) --------------------------------------------------

def _compile_fallback(node: JsltBase) -> Program:
    """Closure de repli : tout nœud non compilé est évalué par l'interpréteur.

    Garantit que le chemin compilé reste toujours correct, même pour un futur
    type de nœud non encore pris en charge ici.
    """
    from .evaluator import JsltEvaluationVisitor

    def prog(ctx: RuntimeContext) -> Any:
        return node.accept(JsltEvaluationVisitor(ctx))

    return prog


_DISPATCH: dict[type, Callable[[Any], Program]] = {
    JsltConstant: _c_constant,
    JsltPath: _c_path,
    JsltVariable: _c_variable,
    JsltObject: _c_object,
    JsltArray: _c_array,
    JsltBinaryOperator: _c_binary,
    JsltOperator: _c_unary,
    JsltFunctionCall: _c_function,
    JsltSwitch: _c_switch,
}
