"""Registre des fonctions jslt (résolution par nom).

Analogue de ``ServiceContainer`` du .NET, simplifié : une fonction est une
callable ``(ctx, *args) -> valeur`` enregistrée sous un nom (insensible à la
casse, comme le ``name.ToLower()`` du .NET).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

JsltFunction = Callable[..., Any]


class FunctionRegistry:
    """Table nom -> fonction, avec les positions d'arguments « chemin »."""

    def __init__(self) -> None:
        self._functions: dict[str, JsltFunction] = {}
        self._path_args: dict[str, tuple[int, ...]] = {}

    def register(
        self, name: str, function: JsltFunction, path_args: tuple[int, ...] = ()
    ) -> None:
        key = name.lower()
        self._functions[key] = function
        self._path_args[key] = path_args

    def get(self, name: str) -> JsltFunction | None:
        return self._functions.get(name.lower())

    def path_args_of(self, name: str) -> tuple[int, ...]:
        """Indices des arguments passés comme chemin JSONPath brut (non évalué)."""
        return self._path_args.get(name.lower(), ())

    def __contains__(self, name: str) -> bool:
        return name.lower() in self._functions


#: Registre par défaut, peuplé par :mod:`jslt.functions.builtins`.
default_registry = FunctionRegistry()


def jslt_function(
    name: str, path_args: tuple[int, ...] = ()
) -> Callable[[JsltFunction], JsltFunction]:
    """Décorateur enregistrant une fonction intégrée dans le registre par défaut.

    ``path_args`` liste les indices d'arguments (0 = premier argument du template)
    reçus comme chemin JSONPath compilé plutôt que comme valeur évaluée.
    """

    def decorator(function: JsltFunction) -> JsltFunction:
        default_registry.register(name, function, path_args)
        return function

    return decorator
