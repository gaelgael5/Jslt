"""Résolution des variables : chaîne de scopes lexicaux.

Port de ``Bb.Jslt.VariableResolver`` et ``Bb.Jslt.VariableManager`` : chaque
scope possède son dictionnaire local et pointe vers un scope parent (``next``).
La résolution d'un nom cherche localement puis remonte la chaîne — ce qui donne
une portée lexicale correcte pour les objets imbriqués.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class VariableResolver(ABC):
    """Maillon de la chaîne de résolution (port de ``VariableResolver``)."""

    def __init__(self, next_resolver: VariableResolver | None = None) -> None:
        self._next = next_resolver

    def get(self, key: str) -> tuple[bool, Any]:
        """Résout ``key`` : renvoie ``(trouvé, valeur)``, en remontant la chaîne."""
        found, result = self._get_impl(key)
        if found:
            return True, result
        if self._next is not None:
            return self._next.get(key)
        return False, None

    @abstractmethod
    def _get_impl(self, key: str) -> tuple[bool, Any]:
        """Résolution locale (sans la chaîne)."""

    def set_next(self, resolver: VariableResolver) -> None:
        if self._next is None:
            self._next = resolver
        else:
            self._next.set_next(resolver)


class VariableManager(VariableResolver):
    """Scope de variables à dictionnaire (port de ``VariableManager``)."""

    def __init__(self, next_resolver: VariableResolver | None = None) -> None:
        super().__init__(next_resolver)
        self._datas: dict[str, Any] = {}

    def add(self, key: str, value: Any) -> None:
        self._datas[key] = value

    def add_many(self, variables: dict[str, Any] | None) -> None:
        if variables:
            self._datas.update(variables)

    def delete(self, key: str) -> None:
        self._datas.pop(key, None)

    def _get_impl(self, key: str) -> tuple[bool, Any]:
        if key in self._datas:
            return True, self._datas[key]
        return False, None
