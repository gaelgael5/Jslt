"""jslt — portage Python du langage JSLT (JSON Stylesheet Language Transformations).

API publique :

    >>> from urban_json import JsltTemplate
    >>> template = JsltTemplate.parse('{ "name": "x" }')
    >>> template.transform({})
    {'name': 'x'}

État d'avancement du portage (cœur) :
    * Phase 0 — analyse syntaxique (parser ANTLR)                [FAIT]
    * Phase 1 — AST + transformation « défaut »                 [FAIT]
    * Phase 2a — JSONPath simple                                 [FAIT]
    * Phase 2b — variables (déclaration, référence, projection)  [FAIT]
    * Phase 3a — boucles ($source / $where)                      [FAIT]
    * Phase 3b — opérateurs (arithmétique, comparaison, logique) [FAIT]
    * Phase 4a — fonctions (registre) + chaînage ->              [FAIT]
    * Phase 4b — casts (#type via convert)                       [FAIT]
    * Phase 4c — when / switch                                   [FAIT]
    * Phase 5a — JSONPath : wildcard, descente .., slices        [FAIT]
    * Phase 5b — JSONPath : filtres ?(...) (comparaisons/logiques)[FAIT]

Restent hors périmètre « cœur » (extensibles) : opérateurs ensemblistes de
filtre (in/nin/subsetof/contains/size/empty) et fonctions de chemin, ainsi que
les fonctions d'E-S (csv, http, hash, randoms, group, sql).
"""

from __future__ import annotations

from typing import Any

from .ast import JsltBase
from .errors import JsltError, JsltSemanticError, JsltSyntaxError
from .functions import (
    FunctionInfo,
    FunctionRegistry,
    ParameterInfo,
    default_registry,
    jslt_function,
    load_plugins,
)
from .parsing import parse_to_tree
from .parsing.script_builder_visitor import ScriptBuilderVisitor
from .runtime import JsltEvaluationVisitor, RuntimeContext, Sources, compile_program
from .runtime.compiler import Program
from .runtime.debug import DebugResult, TraceStep, evaluate_with_trace
from .serialization import to_source

__all__ = [
    "DebugResult",
    "FunctionInfo",
    "FunctionRegistry",
    "JsltError",
    "JsltSemanticError",
    "JsltSyntaxError",
    "JsltTemplate",
    "ParameterInfo",
    "Program",
    "TraceStep",
    "default_registry",
    "jslt_function",
    "load_plugins",
]

__version__ = "0.0.1"

# Chargement paresseux (une fois) des plugins tiers dans le registre par défaut.
_default_plugins_loaded = False


def _ensure_default_plugins() -> None:
    global _default_plugins_loaded
    if not _default_plugins_loaded:
        load_plugins(default_registry)
        _default_plugins_loaded = True


class JsltTemplate:
    """Un template jslt compilé, prêt à transformer des documents JSON.

    On n'instancie pas la classe directement : on passe par :meth:`parse`.
    """

    def __init__(self, ast: JsltBase, source: str) -> None:
        self._ast = ast
        self._source = source
        #: Programme compilé (closures) si :meth:`build` a été appelé, sinon None.
        self._compiled: Program | None = None

    @property
    def ast(self) -> JsltBase:
        """AST jslt construit à partir du template."""
        return self._ast

    @classmethod
    def parse(cls, template: str) -> JsltTemplate:
        """Analyse un template jslt et construit son AST.

        Args:
            template: le template jslt sous forme de chaîne.

        Returns:
            Un :class:`JsltTemplate` prêt à l'emploi.

        Raises:
            JsltSyntaxError: si le template est syntaxiquement invalide.
            JsltSemanticError: si le template est sémantiquement invalide.
        """
        tree = parse_to_tree(template)
        builder = ScriptBuilderVisitor()
        ast = builder.visit(tree)
        return cls(ast, template)

    def build(self) -> JsltTemplate:
        """Compile l'AST en closures pour accélérer les transformations en masse.

        Optionnel. Par défaut, :meth:`transform` utilise l'interpréteur d'AST, qui
        suffit à la grande majorité des cas. Pour des transformations répétées sur
        de gros volumes (imports en masse), ``build()`` pré-compile le template une
        fois : les appels suivants à :meth:`transform` empruntent alors un chemin
        d'exécution plus rapide (sans double-dispatch ni tests de type par nœud),
        pour un résultat **identique**.

        Idempotent. Renvoie ``self`` pour permettre
        ``JsltTemplate.parse(src).build()``.

        Returns:
            Le template lui-même (compilé).
        """
        if self._compiled is None:
            self._compiled = compile_program(self._ast)
        return self

    def transform(
        self, source: Any = None, functions: FunctionRegistry | None = None
    ) -> Any:
        """Applique le template au document source et renvoie le résultat.

        Args:
            source: le document source (structures Python issues de ``json.loads``).
            functions: registre de fonctions à utiliser. Par défaut, le registre
                global (fonctions intégrées + plugins découverts). Passer un
                registre dédié permet d'isoler/limiter les fonctions disponibles.

        Returns:
            Le document transformé (structures Python).
        """
        if functions is None:
            _ensure_default_plugins()
            functions = default_registry
        context = RuntimeContext(Sources(source), functions)
        # Chemin compilé si build() a été appelé (identique, plus rapide en masse) ;
        # sinon l'interpréteur d'AST. Le registre de fonctions reste résolu à
        # l'exécution : un `functions=` par appel est honoré dans les deux cas.
        if self._compiled is not None:
            return self._compiled(context)
        evaluator = JsltEvaluationVisitor(context)
        return self._ast.accept(evaluator)

    def debug(
        self,
        source: Any = None,
        functions: FunctionRegistry | None = None,
        break_functions: Any = (),
        break_lines: Any = (),
        max_steps: int = 10_000,
    ) -> DebugResult:
        """Évalue le template en collectant une trace pas-à-pas (débogage).

        Interpréteur oblige, le débogage se fait au **niveau du template** (pas de
        code généré comme en .NET) : chaque nœud évalué produit une étape
        (:class:`~urban_json.runtime.debug.TraceStep`) avec sa localisation, la source
        courante et la valeur produite.

        Args:
            source: le document source.
            functions: registre de fonctions (défaut : registre global).
            break_functions: noms de fonctions (« méthodes du contexte ») sur
                lesquelles marquer un point d'arrêt.
            break_lines: lignes du template sur lesquelles marquer un point d'arrêt.
            max_steps: nombre maximal d'étapes collectées (garde-fou).

        Returns:
            Un :class:`~urban_json.runtime.debug.DebugResult` (résultat, étapes, erreur).
        """
        if functions is None:
            _ensure_default_plugins()
            functions = default_registry
        context = RuntimeContext(Sources(source), functions)
        return evaluate_with_trace(
            self._ast, context, break_functions, break_lines, max_steps
        )

    def to_source(self) -> str:
        """Re-sérialise l'AST du template en texte source ré-analysable.

        Analogue du ``ToString`` du .NET : le résultat est un template valide,
        équivalent en comportement à l'original (pas forcément identique au
        caractère près — voir :mod:`urban_json.serialization`).

        Returns:
            Le template jslt sérialisé depuis l'AST.
        """
        return to_source(self._ast)
