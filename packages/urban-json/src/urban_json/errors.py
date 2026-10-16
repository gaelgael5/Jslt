"""Exceptions publiques de la librairie jslt."""

from __future__ import annotations


class JsltError(Exception):
    """Classe de base de toutes les erreurs jslt."""


class JsltSemanticError(JsltError):
    """Erreur sémantique détectée lors de la construction de l'AST.

    Par exemple : nom de propriété dupliqué, valeur manquante. Distincte d'une
    erreur purement syntaxique (:class:`JsltSyntaxError`).
    """

    def __init__(self, message: str, *, location: object | None = None) -> None:
        self.location = location
        super().__init__(message)


class JsltSyntaxError(JsltError):
    """Erreur de syntaxe lors de l'analyse d'un template jslt.

    Attributs:
        line: ligne (1-indexée) où l'erreur a été détectée.
        column: colonne (0-indexée) où l'erreur a été détectée.
        offending: texte fautif, lorsqu'il est disponible.
    """

    def __init__(
        self,
        message: str,
        *,
        line: int | None = None,
        column: int | None = None,
        offending: str | None = None,
    ) -> None:
        self.line = line
        self.column = column
        self.offending = offending
        location = ""
        if line is not None:
            location = f" (ligne {line}, colonne {column})"
        super().__init__(f"{message}{location}")
