"""Nœud de résultat d'une évaluation JSONPath.

Port de ``Bb.JPaths.Node`` : une valeur JSON accompagnée de sa localisation
(chemin normalisé depuis la racine). La localisation sert à la descente
récursive et à l'ordre des résultats, et prépare les phases ultérieures.

Les valeurs JSON sont les structures Python natives (dict, list, str, int,
float, bool, None).
"""

from __future__ import annotations

from typing import Any

#: Localisation d'un nœud : suite de clés (str) et d'indices (int) depuis la racine.
NodePath = tuple


class Node:
    """Valeur JSON localisée dans le document."""

    __slots__ = ("location", "value")

    def __init__(self, value: Any, location: NodePath = ()) -> None:
        self.value = value
        self.location = location

    def child(self, value: Any, segment: Any) -> Node:
        """Crée un nœud enfant en étendant la localisation (port de Location.Append)."""
        return Node(value, (*self.location, segment))

    def __repr__(self) -> str:
        return f"Node({self.value!r} @ {self.location!r})"
