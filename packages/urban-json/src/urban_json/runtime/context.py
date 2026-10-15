"""Contexte d'exécution d'une transformation jslt.

Port conceptuel de ``Bb.Jslt.Sources`` et ``Bb.Jslt.RuntimeContext`` : les
documents source d'un côté, l'état d'exécution (source courante, variables) de
l'autre. Les valeurs JSON sont représentées par les structures Python natives
(dict, list, str, int, float, bool, None), telles que produites par
``json.loads``.
"""

from __future__ import annotations

from typing import Any

from urban_json.functions import FunctionRegistry, default_registry

from .variables import VariableManager


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

    Contient le document source courant et le scope de variables courant (chaîne
    de résolveurs, cf. :mod:`urban_json.runtime.variables`).
    """

    def __init__(
        self, sources: Sources | None = None, functions: FunctionRegistry | None = None
    ) -> None:
        self.sources = sources if sources is not None else Sources()
        self.variables = VariableManager()
        self.functions = functions if functions is not None else default_registry
        # Pile de la source courante (``RootSource`` en .NET). Le sommet est la
        # source contre laquelle les chemins JSONPath se résolvent ; elle change
        # dans les boucles et les objets porteurs d'un ``$source``.
        self._source_stack: list[Any] = [self.sources.source]

    @property
    def current_source(self) -> Any:
        """Source courante : sommet de la pile (racine en l'absence de boucle)."""
        return self._source_stack[-1]

    def push_source(self, source: Any) -> None:
        """Empile une nouvelle source courante (entrée dans une boucle / un $source)."""
        self._source_stack.append(source)

    def pop_source(self) -> None:
        """Dépile la source courante pour revenir à la précédente."""
        if len(self._source_stack) > 1:
            self._source_stack.pop()

    def push_scope(self) -> VariableManager:
        """Empile un nouveau scope de variables chaîné au scope courant.

        Renvoie le scope *précédent* : l'appelant le conserve et le restaure en
        fin de portée (voir l'évaluateur), ce qui évite d'exposer le chaînage
        interne.
        """
        previous = self.variables
        self.variables = VariableManager(previous)
        return previous

    def restore_scope(self, previous: VariableManager) -> None:
        """Restaure un scope précédemment renvoyé par :meth:`push_scope`."""
        self.variables = previous
