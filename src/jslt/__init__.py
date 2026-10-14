"""jslt — portage Python du langage JSLT (JSON Stylesheet Language Transformations).

API publique :

    >>> from jslt import JsltTemplate
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
    * Phase 4 — fonctions + when/switch + casts (#type)          [à venir]
    * Phase 5 — JSONPath avancé                                  [à venir]
"""

from __future__ import annotations

from typing import Any

from .ast import JsltBase
from .errors import JsltError, JsltSemanticError, JsltSyntaxError
from .parsing import parse_to_tree
from .parsing.script_builder_visitor import ScriptBuilderVisitor
from .runtime import JsltEvaluationVisitor, RuntimeContext, Sources

__all__ = [
    "JsltError",
    "JsltSemanticError",
    "JsltSyntaxError",
    "JsltTemplate",
]

__version__ = "0.0.1"


class JsltTemplate:
    """Un template jslt compilé, prêt à transformer des documents JSON.

    On n'instancie pas la classe directement : on passe par :meth:`parse`.
    """

    def __init__(self, ast: JsltBase, source: str) -> None:
        self._ast = ast
        self._source = source

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

    def transform(self, source: Any = None) -> Any:
        """Applique le template au document source et renvoie le résultat.

        Args:
            source: le document source (structures Python issues de ``json.loads``).

        Returns:
            Le document transformé (structures Python).
        """
        context = RuntimeContext(Sources(source))
        evaluator = JsltEvaluationVisitor(context)
        return self._ast.accept(evaluator)
