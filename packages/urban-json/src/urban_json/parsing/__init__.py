"""Analyse syntaxique des templates jslt (front-end ANTLR).

Deux étapes, exposées séparément parce que des intégrations s'y branchent :
``parse_to_tree`` rend l'arbre d'analyse ANTLR, ``ScriptBuilderVisitor`` le
convertit en AST jslt. Le chemin courant reste ``JsltTemplate.parse``, qui
enchaîne les deux ; ces deux noms sont là pour qui doit inspecter ou outiller un
template (cf. ``docs/integration.md``).
"""

from .antlr_parser import parse_to_tree
from .script_builder_visitor import ScriptBuilderVisitor

__all__ = ["ScriptBuilderVisitor", "parse_to_tree"]
