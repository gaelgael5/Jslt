"""Contexte d'exécution d'une transformation jslt.

Port conceptuel de ``Bb.Jslt.Sources`` et ``Bb.Jslt.RuntimeContext`` : les
documents source d'un côté, l'état d'exécution (source courante, variables) de
l'autre. Les valeurs JSON sont représentées par les structures Python natives
(dict, list, str, int, float, bool, None), telles que produites par
``json.loads``.
"""

from __future__ import annotations

from typing import Any


class Sources:
    """Jeu de documents source d'une transformation.

    Pour l'instant un unique document source est géré (cas courant). La structure
    laisse la place à plusieurs sources nommées pour les phases ultérieures.
    """

    def __init__(self, source: Any = None) -> None:
        self._source = source

    def set_source(self, source: Any) -> Sources:
        self._source = source
        return self

    @property
    def source(self) -> Any:
        return self._source


class RuntimeContext:
    """État d'exécution porté le long du parcours de l'AST.

    Contient le document source courant et l'environnement de variables. Les
    variables ne sont pas encore alimentées (Phase 2) mais l'état est en place.
    """

    def __init__(self, sources: Sources | None = None) -> None:
        self.sources = sources if sources is not None else Sources()
        self.variables: dict[str, Any] = {}

    @property
    def current_source(self) -> Any:
        """Document source courant (racine, en l'absence de boucle active)."""
        return self.sources.source
