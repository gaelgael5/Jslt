"""Localisation d'un nœud dans le texte source.

Port simplifié de ``Bb.Analysis.DiagTraces.TextLocation`` tel qu'utilisé par les
nœuds Ast (propriété ``Location``). On conserve l'information utile au
diagnostic : ligne, colonne et bornes d'indices dans la source.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TextLocation:
    """Position d'un nœud dans le texte du template (1-indexée pour la ligne)."""

    line: int
    column: int
    start_index: int
    stop_index: int

    @classmethod
    def from_ctx(cls, ctx) -> TextLocation:
        """Construit une TextLocation depuis un contexte d'analyse ANTLR.

        Équivalent de l'extension .NET ``context.ToLocation()``.
        """
        start = ctx.start
        stop = ctx.stop if ctx.stop is not None else start
        return cls(
            line=start.line,
            column=start.column,
            start_index=start.start,
            stop_index=stop.stop,
        )
