"""Front-end ANTLR : texte d'un template jslt -> arbre d'analyse ANTLR.

Ce module encapsule le lexer/parser généré (``jslt._antlr``) et transforme les
erreurs de syntaxe ANTLR en :class:`jslt.errors.JsltSyntaxError`.

À ce stade (Phase 0), on expose uniquement l'arbre d'analyse ANTLR brut. La
construction de l'AST métier interviendra dans la phase suivante.
"""

from __future__ import annotations

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from jslt._antlr.JsltLexer import JsltLexer
from jslt._antlr.JsltParser import JsltParser
from jslt.errors import JsltSyntaxError


class _RaisingErrorListener(ErrorListener):
    """Convertit la première erreur de syntaxe ANTLR en JsltSyntaxError.

    ANTLR, par défaut, écrit les erreurs sur la sortie standard et poursuit
    l'analyse. Pour une librairie, on veut au contraire échouer explicitement.
    """

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        offending = getattr(offendingSymbol, "text", None)
        raise JsltSyntaxError(msg, line=line, column=column, offending=offending)


def parse_to_tree(text: str) -> JsltParser.ScriptContext:
    """Analyse un template jslt et renvoie l'arbre d'analyse ANTLR (règle ``script``).

    Args:
        text: le template jslt sous forme de chaîne.

    Returns:
        Le contexte de la règle de départ ``script``.

    Raises:
        JsltSyntaxError: si le template est syntaxiquement invalide.
    """
    listener = _RaisingErrorListener()

    lexer = JsltLexer(InputStream(text))
    lexer.removeErrorListeners()
    lexer.addErrorListener(listener)

    tokens = CommonTokenStream(lexer)

    parser = JsltParser(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(listener)

    return parser.script()
