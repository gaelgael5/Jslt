"""Pattern Visitor sur l'arbre jslt.

Port de :
    * ``Bb.Contracts.IJsltJsonVisitor``  -> :class:`JsltJsonVisitor`
    * ``Bb.Jslt.Visitors.JsltBaseVisitor`` -> :class:`JsltBaseVisitor`

Correspondance des méthodes (.NET -> Python) :
    VisitObject   -> visit_object
    VisitArray    -> visit_array
    VisitProperty -> visit_property
    VisitConstant -> visit_constant
    VisitJPath    -> visit_jpath
    VisitJVariable-> visit_jvariable

L'interface est volontairement enrichie phase par phase, au rythme de l'ajout
des nœuds AST (variables, chemins, fonctions, opérateurs, switch…), pour éviter
des méthodes se référant à des nœuds encore absents.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .nodes import (
        JsltArray,
        JsltConstant,
        JsltObject,
        JsltPath,
        JsltProperty,
        JsltVariable,
    )


class JsltJsonVisitor(ABC):
    """Interface de visiteur de l'arbre jslt (port de ``IJsltJsonVisitor``)."""

    @abstractmethod
    def visit_object(self, node: JsltObject) -> Any: ...

    @abstractmethod
    def visit_array(self, node: JsltArray) -> Any: ...

    @abstractmethod
    def visit_property(self, node: JsltProperty) -> Any: ...

    @abstractmethod
    def visit_constant(self, node: JsltConstant) -> Any: ...

    @abstractmethod
    def visit_jpath(self, node: JsltPath) -> Any: ...

    @abstractmethod
    def visit_jvariable(self, node: JsltVariable) -> Any: ...


class JsltBaseVisitor(JsltJsonVisitor):
    """Marcheur de base : parcourt les enfants et renvoie le nœud.

    Port de ``Bb.Jslt.Visitors.JsltBaseVisitor``. Les visiteurs concrets
    (évaluation, sérialisation…) héritent de cette classe et surchargent les
    méthodes utiles. Comme en .NET, chaque méthode visite d'abord ``where`` puis
    ``source`` avant les enfants propres au nœud.
    """

    def visit_object(self, node: JsltObject) -> Any:
        if node.where is not None:
            node.where.accept(self)
        if node.source is not None:
            node.source.accept(self)
        for prop in node.properties:
            prop.accept(self)
        return node

    def visit_array(self, node: JsltArray) -> Any:
        if node.where is not None:
            node.where.accept(self)
        if node.source is not None:
            node.source.accept(self)
        for item in node.items:
            item.accept(self)
        return node

    def visit_property(self, node: JsltProperty) -> Any:
        if node.where is not None:
            node.where.accept(self)
        if node.source is not None:
            node.source.accept(self)
        if node.value is not None:
            node.value.accept(self)
        return node

    def visit_constant(self, node: JsltConstant) -> Any:
        if node.where is not None:
            node.where.accept(self)
        if node.source is not None:
            node.source.accept(self)
        return node

    def visit_jpath(self, node: JsltPath) -> Any:
        if node.where is not None:
            node.where.accept(self)
        if node.source is not None:
            node.source.accept(self)
        return node

    def visit_jvariable(self, node: JsltVariable) -> Any:
        if node.where is not None:
            node.where.accept(self)
        if node.source is not None:
            node.source.accept(self)
        if node.value is not None:
            node.value.accept(self)
        return node
