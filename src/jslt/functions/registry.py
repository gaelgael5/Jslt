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
    """Table nom -> fonction."""

    def __init__(self) -> None:
        self._functions: dict[str, JsltFunction] = {}

    def register(self, name: str, function: JsltFunction) -> None:
        self._functions[name.lower()] = function

    def get(self, name: str) -> JsltFunction | None:
        return self._functions.get(name.lower())

    def __contains__(self, name: str) -> bool:
        return name.lower() in self._functions


#: Registre par défaut, peuplé par :mod:`jslt.functions.builtins`.
default_registry = FunctionRegistry()


def jslt_function(name: str) -> Callable[[JsltFunction], JsltFunction]:
    """Décorateur enregistrant une fonction intégrée dans le registre par défaut."""

    def decorator(function: JsltFunction) -> JsltFunction:
        default_registry.register(name, function)
        return function

    return decorator
