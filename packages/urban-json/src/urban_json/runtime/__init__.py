"""Exécution d'un template jslt : contexte + interpréteur d'AST.

En .NET l'exécution passe par de la génération puis compilation de code
(Roslyn). Le portage Python retient un **interpréteur d'AST** (tree-walking) :
plus simple, portable et testable, pour un comportement identique.
"""

from .compiler import Program, compile_program
from .context import RuntimeContext, Sources
from .evaluator import JsltEvaluationVisitor

__all__ = [
    "JsltEvaluationVisitor",
    "Program",
    "RuntimeContext",
    "Sources",
    "compile_program",
]
