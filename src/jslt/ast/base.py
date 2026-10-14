"""Nœud de base de l'arbre jslt.

Port de ``Bb.Jslt.Asts.JsltBase`` (Jslt/Asts/JsltBase.cs).

Patterns repris du code .NET :
    * **Visitor à double dispatch** : chaque nœud implémente ``accept(visitor)``
      qui appelle la méthode ``visit_*`` correspondante du visiteur.
    * Propriétés communes ``source`` / ``where`` portées par le nœud de base
      (utilisées par les boucles et le filtrage dans les phases ultérieures).
    * ``location``, ``comments`` et ``tags`` pour le diagnostic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import TYPE_CHECKING, Any

from .kind import JsltKind
from .location import TextLocation

if TYPE_CHECKING:
    from .visitor import JsltJsonVisitor


class TagEnum(Enum):
    """Marqueurs posés sur un nœud (port de ``Bb.Jslt.Asts.TagEnum``)."""

    TO_EXECUTE = auto()


class JsltBase(ABC):
    """Nœud abstrait de l'arbre jslt."""

    #: Chaîne de citation JSON (port de la constante .NET ``JsltBase.Quote``).
    QUOTE = '"'

    def __init__(self) -> None:
        self.kind: JsltKind | None = None
        self.source: JsltBase | None = None
        self.where: JsltBase | None = None
        self.location: TextLocation | None = None
        self._comments: list[Any] = []
        self._tags: set[TagEnum] = set()

    @abstractmethod
    def accept(self, visitor: JsltJsonVisitor) -> Any:
        """Accepte un visiteur (double dispatch du pattern Visitor)."""

    @property
    def rule_name(self) -> str:
        """Nom de règle du nœud (port de ``JsltBase.RuleName``)."""
        return type(self).__name__

    @property
    def comments(self) -> list[Any]:
        return self._comments

    def add_comments(self, comments) -> None:
        self._comments.extend(comments)

    def add_tag(self, tag: TagEnum, test: bool = True) -> bool:
        """Ajoute un marqueur ; ne fait rien si ``test`` est faux."""
        if test and tag not in self._tags:
            self._tags.add(tag)
            return True
        return False

    def has_tag(self, tag: TagEnum) -> bool:
        return tag in self._tags

    def del_tag(self, tag: TagEnum) -> bool:
        if tag in self._tags:
            self._tags.discard(tag)
            return True
        return False
